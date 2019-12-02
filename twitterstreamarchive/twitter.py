#!/usr/bin/env python

import logging
import tweepy
import twitterstreamarchive.file_writer
import twitterstreamarchive.transform_tweet


# override tweepy.StreamListener
class MyStreamListener(tweepy.StreamListener):

    def __init__(self, archive_path, api=None):
        super().__init__(api)
        self.archive_path = archive_path

    def on_data(self, raw_data):
        # Run tweet json transformations
        raw_data = twitterstreamarchive.transform_tweet.convert_created_at(raw_data)
        # Save tweet to disk
        twitterstreamarchive.file_writer.write_gzip(self.archive_path, raw_data)

    def on_exception(self, exception):
        logging.info("Unhandled tweepy exception: %s", exception)
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
            my_stream.filter(track=track, locations=locations, stall_warnings=True)
        else:
            logging.debug("Collecting an unfiltered stream")
            my_stream.sample(stall_warnings=True)
