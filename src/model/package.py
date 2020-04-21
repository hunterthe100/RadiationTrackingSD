from typing import List

from src.model.gps_location import GPSLocation
from src.model.part import Part


class Package:
    def __init__(self, package_id: str,
                 package_carrier: str,
                 delivered: int,
                 package_radiation: str):
        self.package_id: str = package_id
        self.package_carrier: str = package_carrier
        self.delivered: bool = delivered == 1
        self.package_radiation: str = package_radiation

        self.parts: List[Part] = []
        self.gps_locations: List[GPSLocation] = []
