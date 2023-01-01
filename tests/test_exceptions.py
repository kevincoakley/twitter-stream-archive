#!/usr/bin/env python

import unittest
import twitterstreamarchive.exceptions

from twitterstreamarchive.exceptions import LocalFileException
from twitterstreamarchive.exceptions import LocalTwitterException


class ExceptionsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_local_file_exception(self):
        with self.assertRaises(
            twitterstreamarchive.exceptions.LocalFileException
        ) as se:
            raise LocalFileException("Test Local File Exception")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Test Local File Exception")

    def test_local_twitter_exception(self):
        with self.assertRaises(
            twitterstreamarchive.exceptions.LocalTwitterException
        ) as se:
            raise LocalTwitterException("Test Local Twitter Exception")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Test Local Twitter Exception")
