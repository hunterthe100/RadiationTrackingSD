from collections import namedtuple
from datetime import datetime
from typing import Dict


class TrackingData:
    def __init__(self, google_json: Dict):
        # TODO format response_json to only relevent data namely response -> routes -> legs
        legs = google_json["routes"]["legs"]
        steps = legs["steps"]

        # Value is given in meters
        self.distance = legs["distance"]["value"]

        # Value is given in seconds
        self.duration = legs["duration"]["value"]
