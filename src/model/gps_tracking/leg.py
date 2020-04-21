from typing import List

from src.model.gps_tracking.step import Step


class Leg:
    def __init__(self, distance, duration, start_location, end_location, steps: List, **kwargs):
        self.distance = distance
        self.duration = duration
        self.start_location = start_location
        self.end_location = end_location
        self.steps = [Step(**step) for step in steps]
