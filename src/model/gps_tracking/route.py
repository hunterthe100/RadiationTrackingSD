from typing import List, Tuple

from src.model.gps_location import GPSPoint3D


class Route:
    def __init__(self):
        self.legs: List[Leg] = []

    @property
    # Total distance in meters
    def total_distance(self) -> int:
        return sum([leg.distance for leg in self.legs])

    @property
    # Total duration of route in seconds
    def total_duration(self) -> int:
        return sum([leg.duration for leg in self.legs])


class Leg:
    def __init__(self):
        self.steps: List[Step] = None
        self.distance: int = None
        self.duration: int = None


class Step:
    def __init__(self, start_location: GPSPoint3D, end_location: GPSPoint3D, distance: int, duration: int):
        self.start_location: GPSPoint3D = start_location
        self.end_location: GPSPoint3D = end_location
        self.distance: int = distance
        self.duration: int = duration

    @property
    def gps_points(self):
        return self.start_location, self.end_location

    @gps_points.setter
    def gps_points(self, gps_points: Tuple[GPSPoint3D, GPSPoint3D]):
        self.start_location, self.end_location = gps_points
