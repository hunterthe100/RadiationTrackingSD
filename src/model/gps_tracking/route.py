from typing import List

from src.model.gps_tracking.leg import Leg


class Route:
    def __init__(self, legs: List, summary: str, **kwargs):
        self.legs = [Leg(**leg) for leg in legs]
        self.summary: str = summary
