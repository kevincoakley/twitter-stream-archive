#!/usr/bin/env python

import logging
import tweepy
from prometheus_client import Counter
import twitterstreamarchive.file_writer
import twitterstreamarchive.transform_tweet
from twitterstreamarchive.exceptions import LocalTwitterException


# override tweepy.StreamListener
class MyStreamListener(tweepy.StreamListener):

    def __init__(self, archive_path, api=None):
        super().__init__(api)
        self.archive_path = archive_path
        # Initialize the Prometheus tweet_count counter
        self.tweet_count = Counter("tweet_count", "Number of tweet_timeouts tweets")
        self.tweet_disconnects = Counter("tweet_disconnects", "Number of twitter-stream-archive disconnects")
        self.tweet_errors = Counter("tweet_errors", "Number of twitter-stream-archive errors")
        self.tweet_exceptions = Counter("tweet_exceptions", "Number of twitter-stream-archive exceptions")
        self.tweet_timeouts = Counter("tweet_timeouts", "Number of twitter-stream-archive timeouts")
        self.tweet_warnings = Counter("tweet_warnings", "Number of twitter-stream-archive warnings")

    def on_data(self, raw_data):
        # Increment Prometheus tweet_count counter by 1
        self.tweet_count.inc()
        # Run tweet json transformations
        raw_data = twitterstreamarchive.transform_tweet.convert_created_at(raw_data)
        # Save tweet to disk
        twitterstreamarchive.file_writer.write_gzip(self.archive_path, raw_data)
        return

    def on_disconnect(self, notice):
        # Increment Prometheus tweet_disconnects counter by 1
        self.tweet_disconnects.inc()
        return

    def on_error(self, status_code):
        # Increment Prometheus tweet_errors counter by 1
        self.tweet_errors.inc()
        return

    def on_exception(self, exception):
        # Increment Prometheus tweet_exceptions counter by 1
        self.tweet_exceptions.inc()
        return

    def on_timeout(self):
        # Increment Prometheus tweet_timeouts counter by 1
        self.tweet_timeouts.inc()
        return

    def on_warning(self, notice):
        # Increment Prometheus tweet_warnings counter by 1
        self.tweet_warnings.inc()
        return


class Twitter:

    def __init__(self, consumer_token, consumer_token_secret, access_token, access_token_secret):
        # Setup OAuth Authentication
        auth = tweepy.OAuthHandler(consumer_token, consumer_token_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Authenticate to Twitter
        self.api = tweepy.API(auth)

    def stream(self, archive_path, track=None, locations=None):
        my_stream_listener = MyStreamListener(archive_path)
        my_stream = tweepy.Stream(auth=self.api.auth, listener=my_stream_listener)

        # Convert comma separated strings to a list
        if track:
            track = track.split(",")
        # Convert comma separated strings to a list of floats
        if locations:
            locations = [float(x) for x in locations.split(",")]

        # If track or locations is set then create a filtered stream, otherwise capture everything
        if track or locations:
            logging.debug("Collecting a filtered stream with track: %s and locations: %s", track, locations)
            try:
                my_stream.filter(track=track, locations=locations, stall_warnings=True)
            except Exception as ex:
                raise LocalTwitterException("Unhandled streaming exception: %s" % ex) from None
        else:
            logging.debug("Collecting an unfiltered stream")
            try:
                my_stream.sample(stall_warnings=True)
            except Exception as ex:
                raise LocalTwitterException("Unhandled streaming exception: %s" % ex) from None
