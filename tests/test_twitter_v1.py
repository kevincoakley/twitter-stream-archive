#!/usr/bin/env python

import unittest
import mock
from mock import patch
import prometheus_client
import tweepy
import twitterstreamarchive.twitter_v1
from twitterstreamarchive.twitter_v1 import TwitterV1
from twitterstreamarchive.twitter_v1 import MyStreamV1


class TwitterTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('twitterstreamarchive.file_writer.write_gzip')
    @patch('twitterstreamarchive.transform_tweet.convert_created_at')
    def test_my_stream_listener(self, mock_transform, mock_write_gzip):
        my_stream_listener = MyStreamV1("consumer_token", "consumer_token_secret", "access_token", 
                                              "access_token_secret", "/archive_path")

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
    @patch.object(tweepy.Stream, 'filter')
    def test_twitter(self, mock_stream, mock_prom):
        mock_prom.return_value = None

        #
        # Test Tweepy stream with filter
        #

        # Create a Twitter object and authenticate to Twitter's API
        twitter_track = TwitterV1("consumer_token", "consumer_token_secret", "access_token", "access_token_secret")

        # Start streaming Tweets
        twitter_track.stream("/archive_path", track="test,testing,python", locations="1,1,1,1")

        #
        # Test Tweepy stream with filter raises LocalTwitterException (failing test)
        #
        with self.assertRaises(twitterstreamarchive.exceptions.LocalTwitterException) as lte:

            mock_stream.side_effect = Exception('filter exception')

            # Create a Twitter object and authenticate to Twitter's API
            twitter_track = TwitterV1("consumer_token", "consumer_token_secret", "access_token", "access_token_secret")

            # Start streaming Tweets
            twitter_track.stream("/archive_path", track="test,testing,python", locations="1,1,1,1")

            the_exception = lte.exception
            self.assertEqual(str(the_exception), "Unhandled streaming exception: filter exception")

        #
        # Test Tweepy stream with sample raises LocalTwitterException (failing test)
        #
        with self.assertRaises(twitterstreamarchive.exceptions.LocalTwitterException) as lte:

            # Create a Twitter object and authenticate to Twitter's API
            twitter_sample = TwitterV1("consumer_token", "consumer_token_secret", "access_token", "access_token_secret")

            # Start streaming Tweets
            twitter_sample.stream("/archive_path")

            the_exception = lte.exception
            self.assertEqual(str(the_exception), "Unhandled streaming exception: sample exception")
