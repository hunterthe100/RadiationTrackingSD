import logging
from time import time
from typing import Dict, Tuple, List

import requests

import app_config
from src.model.gps_location import GPSPoint3D

GOOGLE_MAPS_API_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/elevation/"
OUTPUT_FORMAT = "json"
LOCATIONS = "locations={}"
LOCATION_SEP = "|"
KEY = "key={}"
SEP = "&"
INVALID_REQUEST = "INVALID_REQUEST"


class DataAccessObjectAltitude:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_altitudes(self, gps_points: List[Tuple[float, float]]) -> List[Tuple[float, float, float]]:
        start_time = time()
        altitude_points = self._lookup_altitudes(gps_points)
        self.log.debug(f"Lookup done in {round(time() - start_time, 3)} seconds for {len(altitude_points)} locations")
        return altitude_points

    def _lookup_altitudes(self, gps_points: List[Tuple[float, float]]) -> List[Tuple[float, float, float]]:
        self.log.debug(f"Performing lookup for {len(gps_points)} locations")
        url: str = self._format_url(gps_points)
        response_json = self._make_request(url)
        self.log.debug(f"API returned {response_json}")
        return self._translate_results(response_json)

    @staticmethod
    def _format_url(gps_points: List[Tuple[float, float]]) -> str:
        locations = "|".join(["{},{}".format(*point) for point in gps_points])
        params = LOCATIONS.format(locations) + SEP + KEY.format(app_config.GOOGLE_MAPS_KEY)
        return GOOGLE_MAPS_API_DIRECTIONS_URL + OUTPUT_FORMAT + "?" + params

    def _make_request(self, url: str) -> Dict:
        response: requests.Response = requests.get(url)
        response_json: Dict = response.json()
        if response_json['status'] == INVALID_REQUEST:
            self.log.error(f"Failed API call to {url}")
            raise ValueError(f"Failed API call to {url}")
        return response_json

    @staticmethod
    def _translate_results(response_json: Dict) -> List[Tuple[float, float, float]]:
        gps_3d_points = []
        for result in response_json['results']:
            gps_3d_points.append(GPSPoint3D(result['location']['lat'], result['location']['lng'], result['elevation']))
        return gps_3d_points
