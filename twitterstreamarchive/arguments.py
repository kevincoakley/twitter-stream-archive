#!/usr/bin/env python

import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug',
                        dest="debug",
                        action='store_true')

    parser.add_argument("--consumer-token",
                        metavar="consumer_token",
                        dest="consumer_token",
                        help="Twitter API Consumer Token.",
                        default=os.environ.get('CONSUMER_TOKEN', None))

    parser.add_argument("--consumer-token-secret",
                        metavar="consumer_token_secret",
                        dest="consumer_token_secret",
                        help="Twitter API Consumer Token Secret.",
                        default=os.environ.get('CONSUMER_TOKEN_SECRET', None))

    parser.add_argument("--access-token",
                        metavar="access_token",
                        dest="access_token",
                        help="Twitter API Access Token.",
                        default=os.environ.get('ACCESS_TOKEN', None))

    parser.add_argument("--access-token-secret",
                        metavar="access_token_secret",
                        dest="access_token_secret",
                        help="Twitter API Access Token Secret.",
                        default=os.environ.get('ACCESS_TOKEN_SECRET', None))

    parser.add_argument("--archive-path",
                        metavar="archive_path",
                        dest="archive_path",
                        help="Path to Save Archived Tweets.",
                        default=os.environ.get('ARCHIVE_PATH', None))

    parser.add_argument("--stream-track",
                        metavar="stream_track",
                        dest="stream_track",
                        help="Comma Separated List of Terms to Apply to the Stream Filter.",
                        default=os.environ.get('STREAM_TRACK', None))

    parser.add_argument("--stream-locations",
                        metavar="stream_locations",
                        dest="stream_locations",
                        help="Comma Separated List of Geo Coordinates to Apply to the Stream "
                             "Filter.",
                        default=os.environ.get('STREAM_LOCATIONS', None))

    return vars(parser.parse_args())
