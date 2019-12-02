#!/usr/bin/env python

import datetime
import json
import logging


def convert_created_at(status):
    status_json = json.loads(status)

    # Convert "Wed Nov 27 23:27:39 +0000 2019" to "2019-11-27 23:27:39"
    if "created_at" in status_json:
        created_at = status_json["created_at"]
        # Convert created_at to a datetime object
        created_at_in_datetime = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        # Convert created_at_in_datetime object to the new format
        created_at_converted = created_at_in_datetime.strftime("%Y-%m-%d %H:%M:%S")
    else:
        # If status is a delete status then just return status
        if "delete" in status_json:
            return status
        # If status is not a delete status then there is probably an error
        logging.info("Tweet does not have a created_at variable: %s", status)
        return status

    # Add the created_at_converted element to the json
    status_json["created_at_converted"] = created_at_converted

    return json.dumps(status_json)
