#!/usr/bin/env python

import json
import unittest
import twitterstreamarchive.transform_tweet


class TransformTweetTestCase(unittest.TestCase):

    def setUp(self):
        with open("tests/test_files/tweet.json", 'rt') as f:
            for line in f:
                self.status = line

        with open("tests/test_files/tweet_convert_created_at.json", 'rt') as f:
            for line in f:
                self.test_status_convert_created_at = line

    def test_convert_created_at(self):
        #
        # Test normal tweet
        #
        status_convert_created_at = \
            twitterstreamarchive.transform_tweet.convert_created_at(self.status)

        self.assertEqual(json.loads(status_convert_created_at),
                         json.loads(self.test_status_convert_created_at))

        #
        # Test delete tweet
        #
        delete_tweet = '{"delete":{"status":{"id":123,"id_str":"123","user_id":321,"user_id_str":"321"},' \
                       '"timestamp_ms":"000"}}'

        delete_convert_created_at = \
            twitterstreamarchive.transform_tweet.convert_created_at(delete_tweet)

        self.assertEqual(json.loads(delete_tweet), json.loads(delete_convert_created_at))

        #
        # Test unknown tweet
        #
        unknown_tweet = '{"status":{"id":123,"id_str":"123","user_id":321,"user_id_str":"321"},"timestamp_ms":"000"}'

        unknown_convert_created_at = \
            twitterstreamarchive.transform_tweet.convert_created_at(unknown_tweet)

        self.assertEqual(json.loads(unknown_tweet), json.loads(unknown_convert_created_at))
