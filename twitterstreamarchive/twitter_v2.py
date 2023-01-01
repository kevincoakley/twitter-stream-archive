#!/usr/bin/env python

import logging
import tweepy
from prometheus_client import Counter
import twitterstreamarchive.file_writer
import twitterstreamarchive.transform_tweet
from twitterstreamarchive.exceptions import LocalTwitterException

logger = logging.getLogger("twitterstreamarchive.twitter")


# override tweepy.StreamingClient
class MyStreamingClientv2(tweepy.StreamingClient):
    def __init__(self, bearer_token, archive_path):
        """
        :param bearer_token: twitter bearer token
        :param archive_path: directory to save the twitter statuses to
        """
        super().__init__(bearer_token)
        self.archive_path = archive_path
        # Initialize the Prometheus tweet_count counter
        self.tweet_count = Counter("tweet_count", "Number of tweet_timeouts tweets")
        self.tweet_disconnects = Counter(
            "tweet_disconnects", "Number of twitter-stream-archive disconnects"
        )
        self.tweet_errors = Counter(
            "tweet_errors", "Number of twitter-stream-archive errors"
        )
        self.tweet_exceptions = Counter(
            "tweet_exceptions", "Number of twitter-stream-archive exceptions"
        )
        self.tweet_timeouts = Counter(
            "tweet_timeouts", "Number of twitter-stream-archive timeouts"
        )
        self.tweet_warnings = Counter(
            "tweet_warnings", "Number of twitter-stream-archive warnings"
        )

    def on_data(self, raw_data):
        """
        Called when raw data is received from connection. Return False to stop stream and close connection.

        :param raw_data: raw output from tweepy stream
        """
        # Increment Prometheus tweet_count counter by 1
        self.tweet_count.inc()
        # Run tweet json transformations
        raw_data = twitterstreamarchive.transform_tweet.convert_created_at(
            raw_data.decode("utf-8")
        )
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


class TwitterV2:
    def __init__(self, bearer_token):
        """
        :param bearer_token: twitter bearer token
        """
        self.bearer_token = bearer_token

    def stream(self, archive_path, track=None, locations=None):
        """
        :param archive_path: directory to save the twitter statuses to
        :param track: list of keywords to filter (optional)
        :param locations: list of lat/long box to filter (optional)
        """
        # See https://developer.twitter.com/en/docs/twitter-api/tweets/volume-streams/api-reference/get-tweets-sample-stream
        expansions = [
            "attachments.media_keys",
            "geo.place_id",
            "attachments.poll_ids",
            "author_id",
        ]
        tweet_fields = [
            "attachments",
            "author_id",
            "context_annotations",
            "conversation_id",
            "created_at",
            "edit_controls",
            "entities",
            "geo",
            "id",
            "in_reply_to_user_id",
            "lang",
            "public_metrics",
            "possibly_sensitive",
            "referenced_tweets",
            "reply_settings",
            "source",
            "text",
            "withheld",
        ]
        user_fields = [
            "created_at",
            "description",
            "entities",
            "id",
            "location",
            "name",
            "pinned_tweet_id",
            "profile_image_url",
            "protected",
            "public_metrics",
            "url",
            "username",
            "verified",
            "withheld",
        ]
        place_fields = [
            "contained_within",
            "country",
            "country_code",
            "full_name",
            "geo",
            "id",
            "name",
            "place_type",
        ]
        media_fields = [
            "duration_ms",
            "height",
            "media_key",
            "preview_image_url",
            "type",
            "url",
            "width",
            "public_metrics",
            "alt_text",
            "variants",
        ]
        poll_fields = [
            "duration_minutes",
            "end_datetime",
            "id",
            "options",
            "voting_status",
        ]

        my_stream = MyStreamingClientv2(self.bearer_token, archive_path)

        # If track or locations is set then create a filtered stream, otherwise capture everything
        if track or locations:
            logger.debug(
                "Tracking Twitter streams by keyword or location not supported yet"
            )
            raise LocalTwitterException(
                "Tracking Twitter streams by keyword or location not supported yet"
            )
        else:
            logger.debug("Collecting an unfiltered stream")
            try:
                my_stream.sample(
                    expansions=expansions,
                    tweet_fields=tweet_fields,
                    user_fields=user_fields,
                    place_fields=place_fields,
                    media_fields=media_fields,
                    poll_fields=poll_fields,
                )
            except Exception as ex:
                raise LocalTwitterException(
                    "Unhandled streaming exception: %s" % ex
                ) from None
