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
        status_convert_created_at = \
            twitterstreamarchive.transform_tweet.convert_created_at(self.status)

        self.assertEqual(json.loads(status_convert_created_at),
                         json.loads(self.test_status_convert_created_at))
