#!/usr/bin/env python

import datetime
import gzip
import logging


def write_gzip(archive_path, status):
    try:
        with gzip.open(archive_path + "/" + datetime.datetime.now().strftime("%Y%m%d-%H-tweets.txt.gz"),
                       "at", encoding='utf8') as f:
            f.write(str(status))
    except IOError as ex:
        logging.info("Error writing to archive: %s/%s: %s", archive_path,
                     datetime.datetime.now().strftime("%Y%m%d-%H-tweets.txt.gz"), ex)
