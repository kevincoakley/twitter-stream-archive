#!/usr/bin/env python

import sys
import logging
import prometheus_client
import twitterstreamarchive.arguments
from twitterstreamarchive.twitter import Twitter


def main():
    """
    :return: 0 if successful otherwise return an error message as a string
    """
    args = twitterstreamarchive.arguments.parse_arguments(sys.argv[1:])

    log_level = logging.INFO

    if args.debug is True:
        log_level = logging.DEBUG

    logger = logging.getLogger('twitterstreamarchive')
    logger.setLevel(level=log_level)
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    # Print all arguments for debugging purposes
    logger.debug("consumer_token: %s", args.consumer_token)
    logger.debug("consumer_token_secret: %s", args.consumer_token_secret)
    logger.debug("access_token: %s", args.access_token)
    logger.debug("access_token_secret: %s", args.access_token_secret)
    logger.debug("archive_path: %s", args.archive_path)
    logger.debug("stream_track: %s", args.stream_track)
    logger.debug("stream_locations: %s", args.stream_locations)

    if args.consumer_token is None or args.consumer_token_secret is None or \
            args.access_token is None or args.access_token_secret is None or \
            args.archive_path is None:
        return ('''
twitter-stream-archive requires consumer_token, consumer_token_secret, access_token,
access_token_secret, and archive_path to be set or overridden with --consumer-token,
--consumer-token-secret, --access-token, --access-token-secret, or --archive-path.''')

    # Start the Prometheus server on port 8000
    logger.debug("Starting the Prometheus server on port 8000")
    prometheus_client.start_http_server(8000)

    # Create a Twitter object and authenticate to Twitter's API
    twitter = Twitter(args.consumer_token, args.consumer_token_secret,
                      args.access_token, args.access_token_secret)

    # Start streaming Tweets
    twitter.stream(args.archive_path, track=args.stream_track,
                   locations=args.stream_locations)

    return 0
