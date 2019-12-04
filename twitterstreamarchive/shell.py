#!/usr/bin/env python

import sys
import logging
import twitterstreamarchive.arguments as arguments
from prometheus_client import start_http_server
from twitterstreamarchive.twitter import Twitter


def main():
    args = arguments.parse_arguments()

    log_level = logging.INFO

    if args["debug"] is True:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s',
                        handlers=[logging.StreamHandler()])

    # Print all arguments for debugging purposes
    logging.info("consumer_token: %s", args["consumer_token"])
    logging.info("consumer_token_secret: %s", args["consumer_token_secret"])
    logging.info("access_token: %s", args["access_token"])
    logging.info("access_token_secret: %s", args["access_token_secret"])

    logging.info("archive_path: %s", args["archive_path"])

    logging.info("stream_track: %s", args["stream_track"])
    logging.info("stream_locations: %s", args["stream_locations"])

    # Verify the Twitter API keys have been set
    if args["consumer_token"] is None or args["consumer_token_secret"] is None \
            or args["access_token"] is None or args["access_token_secret"] is None:
        sys.exit("The Twitter API keys must be set!")

    # Verify the archive path has been set
    if args["archive_path"] is None:
        sys.exit("The archive path must be set!")

    # Start the Prometheus server on port 8000
    logging.info("Starting the Prometheus server on port 8000")
    start_http_server(8000)

    # Create a Twitter object and authenticate to Twitter's API
    twitter = Twitter(args["consumer_token"], args["consumer_token_secret"],
                      args["access_token"], args["access_token_secret"])

    # Start streaming Tweets
    twitter.stream(args["archive_path"], track=args["stream_track"],
                   locations=args["stream_locations"])
