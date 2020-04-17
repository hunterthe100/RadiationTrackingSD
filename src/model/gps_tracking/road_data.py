from collections import namedtuple
from datetime import datetime
from typing import Dict


class RoadData:
    def __init__(self, google_json: Dict):
        # TODO format response_json to only relevant data namely response -> routes -> legs

        legs = google_json['routes'][0]['legs'][0]
        steps = legs['steps']

        # Value is given in meters
        self.distance = legs['distance']['value']

        # Value is given in seconds
        self.duration = legs['duration']['value']

        for step in steps:
            print(type(step))
            print(len(step))
            # print(step)
