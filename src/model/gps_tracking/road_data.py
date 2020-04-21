from typing import Dict

from src.model.gps_tracking.route import Route


class RoadData:
    def __init__(self, google_json: Dict):
        self.route = Route(**google_json['routes'][0])

    @property
    # Returns total distance of trip in meters
    def distance(self) -> int:
        return sum([leg.distance['value'] for leg in self.route.legs])

    @property
    # Returns duration of trip in seconds
    def duration(self) -> int:
        return sum([leg.duration['value'] for leg in self.route.legs])

    @property
    def steps(self):
        steps = []
        for leg in self.route.legs:
            steps.extend(leg.steps)
        return steps
