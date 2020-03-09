#!/usr/bin/env python

import datetime
import errno
import gzip

from twitterstreamarchive.exceptions import LocalFileException


def write_gzip(path, status):
    """
    :param path: path to save the status
    :param status: tweet json as string
    """

    file_path = path + "/" + datetime.datetime.now().strftime("%Y%m%d-%H-tweets.txt.gz")

    try:
        with gzip.open(file_path, "at", encoding='utf8') as f:
            f.write(str(status).strip() + "\n")
    except OSError as ex:
        if ex.errno == errno.EACCES:
            raise LocalFileException("Permission error with \"%s\"" % file_path) from None
        else:
            raise LocalFileException("Unknown error with \"%s\": %s" % (file_path, ex.strerror)) from None
