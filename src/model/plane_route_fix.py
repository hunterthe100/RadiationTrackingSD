import logging
from math import radians, cos, sin, asin, sqrt

from src.model.gps_location import GPSPoint

#TODO add route generator for plane
class PlanePathLengthAndAltitude:
    def __init__(self, origin: GPSPoint, destination: GPSPoint):
        self.log = logging.getLogger(self.__class__.__name__)
        self.plane_distance = self._haversine(origin, destination)

    @staticmethod
    def _haversine(self, origin: GPSPoint, destination: GPSPoint) -> float:
        # Convert lat/lon degrees to radians
        points = [origin.Longitude, origin.Latitude, destination.Longitude, destination.Latitude]
        lon1, lat1, lon2, lat2 = map(radians, points)
        # Differences
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        # haversine formula
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km

    @property
    def plane_altitude(self) -> float:
        return 11600.0

    @property
    def plane_speed(self) -> float:
        return self.plane_distance / 267.54
