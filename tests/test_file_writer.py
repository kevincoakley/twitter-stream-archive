#!/usr/bin/env python

import os
import errno
import datetime
import unittest
from mock import patch
import twitterstreamarchive.file_writer


class FilesWriterTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('gzip.open', create=True)
    def test_write_gzip(self, mock_gzip_open):
        #
        # Test write_gzip with no errors
        #
        twitterstreamarchive.file_writer.write_gzip("/test", "tweet")

        mock_gzip_open.assert_called_once_with("/test/" +
                                               datetime.datetime.now().strftime("%Y%m%d-%H-tweets.txt.gz"),
                                               "at", encoding="utf8")
        handle = mock_gzip_open()
        handle.__enter__().write.assert_called_once_with("tweet\n")

        #
        # Test PermissionError raises LocalFileException (failing test)
        #
        mock_gzip_open.side_effect = OSError(errno.EACCES, os.strerror(errno.EACCES), "permission_file")

        with self.assertRaises(twitterstreamarchive.exceptions.LocalFileException) as lfe:
            twitterstreamarchive.file_writer.write_gzip("permission_file", "permission_file")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Permission error with \"permission_file/%s\"" %
                         datetime.datetime.now().strftime("%Y%m%d-%H-tweets.txt.gz"))

        #
        # Test Input/Output Error raises Unknown LocalFileException (failing test)
        #
        mock_gzip_open.side_effect = OSError(errno.EIO, os.strerror(errno.EIO), "io_error")

        with self.assertRaises(twitterstreamarchive.exceptions.LocalFileException) as lfe:
            twitterstreamarchive.file_writer.write_gzip("io_error", "io_error")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Unknown error with \"io_error/%s\": Input/output error" %
                         datetime.datetime.now().strftime("%Y%m%d-%H-tweets.txt.gz"))
