# Library of utilities
# December 21, 2021 v0.01
# IoT for Kids: https://jxsboston.github.io/IoT-Kids/

import requests, json, datetime
from typing import Optional, Dict, Any

# Function to return the current date and time in string based on
#   the YR-MO-DAY-HR-MIN-SEC format.
#
def getCurrentTimeStamp() -> str:
    dt = datetime.datetime.now()
    return "{:d}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

