from typing import List

from src.model.gps_location import GPSLocation
from src.model.part import Part


class Package:
    def __init__(self):

        self.carrier_code: str = None
        self.tracking_number: str = None
        self.route: List = []
        self.
        self.package_radiation: str = package_radiation

        self.parts: List[Part] = []
        self.gps_locations: List[GPSLocation] = []
