#!/usr/bin/env python

import datetime
import json
import logging

logger = logging.getLogger('twitterstreamarchive.transform_tweet')


def convert_created_at(status):
    """
    Add created_at_converted to status to make the status easier to import into postgresql
    :param status: tweet json as string
    :return: tweet json as string with created_at_converted added
    """
    status_json = json.loads(status)

    # Convert "Wed Nov 27 23:27:39 +0000 2019" to "2019-11-27 23:27:39"
    if "created_at" in status_json:
        created_at = status_json["created_at"]
        # Convert created_at to a datetime object
        created_at_in_datetime = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        # Convert created_at_in_datetime object to the new format
        created_at_converted = created_at_in_datetime.strftime("%Y-%m-%d %H:%M:%S")
    else:
        # If status is a delete or a status_withheld status then just return status
        if "delete" in status_json or "status_withheld" in status_json:
            return status
        # If status is not a delete status then there is probably an error
        logger.info("Tweet does not have a created_at variable: %s", status)
        return status

    # Add the created_at_converted element to the json
    status_json["created_at_converted"] = created_at_converted

    return json.dumps(status_json, ensure_ascii=False)
