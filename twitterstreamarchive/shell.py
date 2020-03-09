#!/usr/bin/env python

import sys
import logging
import prometheus_client
import twitterstreamarchive.arguments
from twitterstreamarchive.twitter import Twitter


def main():
    args = twitterstreamarchive.arguments.parse_arguments(sys.argv[1:])

    log_level = logging.INFO

    if args.debug is True:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s',
                        handlers=[logging.StreamHandler()])

    # Print all arguments for debugging purposes
    logging.info("consumer_token: %s", args.consumer_token)
    logging.info("consumer_token_secret: %s", args.consumer_token_secret)
    logging.info("access_token: %s", args.access_token)
    logging.info("access_token_secret: %s", args.access_token_secret)
    logging.info("archive_path: %s", args.archive_path)
    logging.info("stream_track: %s", args.stream_track)
    logging.info("stream_locations: %s", args.stream_locations)

    if args.consumer_token is None or args.consumer_token_secret is None or \
            args.access_token is None or args.access_token_secret is None or \
            args.archive_path is None:
        return ('''
twitter-stream-archive requires consumer_token, consumer_token_secret, access_token,
access_token_secret, and archive_path to be set or overridden with --consumer-token,
--consumer-token-secret, --access-token, --access-token-secret, or --archive-path.''')

    # Start the Prometheus server on port 8000
    logging.info("Starting the Prometheus server on port 8000")
    prometheus_client.start_http_server(8000)

    # Create a Twitter object and authenticate to Twitter's API
    twitter = Twitter(args.consumer_token, args.consumer_token_secret,
                      args.access_token, args.access_token_secret)

    # Start streaming Tweets
    twitter.stream(args.archive_path, track=args.stream_track,
                   locations=args.stream_locations)

    return 0
