#!/usr/bin/env python

import os
import sys
import unittest
from mock import patch
import twitterstreamarchive.shell as shell

from twitterstreamarchive.twitter_v1 import TwitterV1


class ShellTestCase(unittest.TestCase):

    def setUp(self):
        if "CONSUMER_TOKEN" in os.environ:
            del os.environ["CONSUMER_TOKEN"]
        if "CONSUMER_TOKEN_SECRET" in os.environ:
            del os.environ["CONSUMER_TOKEN_SECRET"]
        if "ACCESS_TOKEN" in os.environ:
            del os.environ["ACCESS_TOKEN"]
        if "ACCESS_TOKEN_SECRET" in os.environ:
            del os.environ["ACCESS_TOKEN_SECRET"]
        if "ARCHIVE_PATH" in os.environ:
            del os.environ["ARCHIVE_PATH"]
        if "STREAM_TRACK" in os.environ:
            del os.environ["STREAM_TRACK"]
        if "STREAM_LOCATIONS" in os.environ:
            del os.environ["STREAM_LOCATIONS"]

    @patch('prometheus_client.start_http_server')
    @patch.object(TwitterV1, 'stream')
    @patch.object(TwitterV1, '__init__')
    def test_main(self, mock_twitter, mock_twitter_stream, mock_prom):
        mock_twitter.return_value = None
        mock_twitter_stream.return_value = None
        mock_prom.return_value = None

        #
        # Test that an error message is returned when the required args are not passed
        #
        with patch.object(sys, 'argv', ["twitter-stream-archive", "--consumer-token", "test"]):
            self.assertRegex(shell.main(), "^\ntwitter-stream-archive requires")

        #
        # Test with command line arguments
        #
        with patch.object(sys, 'argv', ["twitter-stream-archive",
                                        "--consumer-token", "test",
                                        "--consumer-token-secret", "test",
                                        "--access-token", "test",
                                        "--access-token-secret", "test",
                                        "--archive-path", "test"]):
            shell.main()

        #
        # Test with environment variables
        #
        os.environ["CONSUMER_TOKEN"] = "test"
        os.environ["CONSUMER_TOKEN_SECRET"] = "test"
        os.environ["ACCESS_TOKEN"] = "test"
        os.environ["ACCESS_TOKEN_SECRET"] = "test"
        os.environ["ARCHIVE_PATH"] = "test"

        with patch.object(sys, 'argv', ["twitter-stream-archive"]):
            shell.main()

        #
        # Test the debug command line argument
        #
        with patch.object(sys, 'argv', ["twitter-stream-archive", "--debug"]):
            shell.main()
