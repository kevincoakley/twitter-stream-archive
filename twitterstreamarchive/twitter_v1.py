#!/usr/bin/env python

import logging
import tweepy
from prometheus_client import Counter
import twitterstreamarchive.file_writer
import twitterstreamarchive.transform_tweet
from twitterstreamarchive.exceptions import LocalTwitterException

logger = logging.getLogger('twitterstreamarchive.twitter')


# override tweepy.Stream
class MyStreamV1(tweepy.Stream):

    def __init__(self, consumer_token, consumer_token_secret, access_token, access_token_secret, archive_path):
        """
        :param consumer_token: twitter api consumer token
        :param consumer_token_secret: twitter api consumer token secret
        :param access_token: twitter api access token
        :param access_token_secret: twitter api access token secret
        :param archive_path: directory to save the twitter statuses to
        """
        super().__init__(consumer_token, consumer_token_secret, access_token, access_token_secret)
        self.archive_path = archive_path
        # Initialize the Prometheus tweet_count counter
        self.tweet_count = Counter("tweet_count", "Number of tweet_timeouts tweets")
        self.tweet_disconnects = Counter("tweet_disconnects", "Number of twitter-stream-archive disconnects")
        self.tweet_errors = Counter("tweet_errors", "Number of twitter-stream-archive errors")
        self.tweet_exceptions = Counter("tweet_exceptions", "Number of twitter-stream-archive exceptions")
        self.tweet_timeouts = Counter("tweet_timeouts", "Number of twitter-stream-archive timeouts")
        self.tweet_warnings = Counter("tweet_warnings", "Number of twitter-stream-archive warnings")

    def on_data(self, raw_data):
        """
        Called when raw data is received from connection. Return False to stop stream and close connection.

        :param raw_data: raw output from tweepy stream
        """
        # Increment Prometheus tweet_count counter by 1
        self.tweet_count.inc()
        # Run tweet json transformations
        raw_data = twitterstreamarchive.transform_tweet.convert_created_at(raw_data)
        # Save tweet to disk
        twitterstreamarchive.file_writer.write_gzip(self.archive_path, raw_data)
        return

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/streaming-message-types

        :param notice: disconnect notice string from tweepy
        """
        # Increment Prometheus tweet_disconnects counter by 1
        self.tweet_disconnects.inc()
        return

    def on_error(self, status_code):
        """
        Called when a non-200 status code is returned

        :param status_code: http status code from tweepy
        """
        # Increment Prometheus tweet_errors counter by 1
        self.tweet_errors.inc()
        return

    def on_exception(self, exception):
        """
        Called when an unhandled exception occurs.

        :param exception: exception from tweepy
        """
        # Increment Prometheus tweet_exceptions counter by 1
        self.tweet_exceptions.inc()
        return

    def on_timeout(self):
        """
        Called when stream connection times out
        """
        # Increment Prometheus tweet_timeouts counter by 1
        self.tweet_timeouts.inc()
        return

    def on_warning(self, notice):
        """
        Called when a disconnection warning message arrive

        :param notice: warning notice string from tweepy
        """
        # Increment Prometheus tweet_warnings counter by 1
        self.tweet_warnings.inc()
        return


class TwitterV1:

    def __init__(self, consumer_token, consumer_token_secret, access_token, access_token_secret):
        """
        :param consumer_token: twitter api consumer token
        :param consumer_token_secret: twitter api consumer token secret
        :param access_token: twitter api access token
        :param access_token_secret: twitter api access token secret
        """
        self.consumer_token = consumer_token
        self.consumer_token_secret = consumer_token_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def stream(self, archive_path, track=None, locations=None):
        """
        :param archive_path: directory to save the twitter statuses to
        :param track: list of keywords to filter (optional)
        :param locations: list of lat/long box to filter (optional)
        """
        # Create a stream listener
        my_stream = MyStreamV1(self.consumer_token, self.consumer_token_secret,
                                     self.access_token, self.access_token_secret, archive_path)

        # Convert comma separated strings to a list
        if track:
            track = track.split(",")
        # Convert comma separated strings to a list of floats
        if locations:
            locations = [float(x) for x in locations.split(",")]

        # If track or locations is set then create a filtered stream, otherwise capture everything
        if track or locations:
            logger.debug("Collecting a filtered stream with track: %s and locations: %s", track, locations)
            try:
                my_stream.filter(track=track, locations=locations, stall_warnings=True)
            except Exception as ex:
                raise LocalTwitterException("Unhandled streaming exception: %s" % ex) from None
        else:
            logger.debug("Collecting an unfiltered stream no longer supported by Twitter v1 API")
            raise LocalTwitterException("Collecting an unfiltered stream no longer supported by Twitter v1 API")
