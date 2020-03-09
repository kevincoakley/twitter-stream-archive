#!/usr/bin/env python

import unittest
import mock
from mock import patch
import prometheus_client
import twitterstreamarchive.twitter
from twitterstreamarchive.twitter import Twitter
from twitterstreamarchive.twitter import MyStreamListener


class TwitterTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('twitterstreamarchive.file_writer.write_gzip')
    @patch('twitterstreamarchive.transform_tweet.convert_created_at')
    def test_my_stream_listener(self, mock_transform, mock_write_gzip):
        my_stream_listener = MyStreamListener("/archive_path")

        mock_transform.return_value = "raw_data"
        mock_write_gzip.return_value = True

        #
        # Test all of the MyStreamListener methods, all should return None
        #
        self.assertEqual(my_stream_listener.on_data("raw_data"), None)
        self.assertEqual(my_stream_listener.on_disconnect("notice"), None)
        self.assertEqual(my_stream_listener.on_error("status_code"), None)
        self.assertEqual(my_stream_listener.on_exception("exception"), None)
        self.assertEqual(my_stream_listener.on_timeout(), None)
        self.assertEqual(my_stream_listener.on_warning("notice"), None)

    @patch.object(prometheus_client.Counter, '__init__')
    @patch('tweepy.Stream', autospec=True)
    def test_twitter(self, mock_stream, mock_prom):
        mock_prom.return_value = None

        #
        # Test Tweepy stream with filter
        #

        # Create a Twitter object and authenticate to Twitter's API
        twitter_track = Twitter("consumer_token", "consumer_token_secret", "access_token", "access_token_secret")

        # Start streaming Tweets
        twitter_track.stream("/archive_path", track="test,testing,python", locations="1,1,1,1")

        #
        # Test Tweepy stream with sample
        #

        # Create a Twitter object and authenticate to Twitter's API
        twitter_sample = Twitter("consumer_token", "consumer_token_secret", "access_token", "access_token_secret")

        # Start streaming Tweets
        twitter_sample.stream("/archive_path")

        #
        # Test Tweepy stream with filter raises LocalFileException (failing test)
        #
        with self.assertRaises(twitterstreamarchive.exceptions.LocalTwitterException) as lte:

            mock_filter = mock.Mock()
            mock_filter.side_effect = Exception('filter exception')
            mock_stream(auth="", listener="").filter = mock_filter

            # Create a Twitter object and authenticate to Twitter's API
            twitter_track = Twitter("consumer_token", "consumer_token_secret", "access_token", "access_token_secret")

            # Start streaming Tweets
            twitter_track.stream("/archive_path", track="test,testing,python", locations="1,1,1,1")

            the_exception = lte.exception
            self.assertEqual(str(the_exception), "Unhandled streaming exception: filter exception")

        #
        # Test Tweepy stream with sample raises LocalFileException (failing test)
        #
        with self.assertRaises(twitterstreamarchive.exceptions.LocalTwitterException) as lte:

            mock_sample = mock.Mock()
            mock_sample.side_effect = Exception('sample exception')
            mock_stream(auth="", listener="").sample = mock_sample

            # Create a Twitter object and authenticate to Twitter's API
            twitter_sample = Twitter("consumer_token", "consumer_token_secret", "access_token", "access_token_secret")

            # Start streaming Tweets
            twitter_sample.stream("/archive_path")

            the_exception = lte.exception
            self.assertEqual(str(the_exception), "Unhandled streaming exception: sample exception")
