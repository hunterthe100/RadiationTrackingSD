import logging
from typing import List, Dict

import requests

import app_config
from src.model.gps_location import GPSPoint

GOOGLE_MAPS_BASE_API_URL = "https://maps.googleapis.com/maps/api/"
GOOGLE_MAPS_ELEVATION_API_URL = GOOGLE_MAPS_BASE_API_URL + "elevation/"
GOOGLE_MAPS_DIRECTION_API_URL = GOOGLE_MAPS_BASE_API_URL + "directions/"
GOOGLE_MAPS_PLACE_API_URL = GOOGLE_MAPS_BASE_API_URL + "place/findplacefromtext/"
GOOGLE_MAPS_PLACE_API_REQUEST_TYPE = "textquery"
FORMAT = "json"
PARAM_SEP = "&"


class GoogleAPICaller:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    # Get route data from google API
    def get_road_data(self, origin: GPSPoint, destination: GPSPoint) -> Dict:
        url = self._format_direction_request_url(origin, destination)
        result = self._make_request(url)
        return result

    # Get GPS point data from google API
    def get_elevations(self, gps_points: List[GPSPoint]) -> Dict:
        url = self._format_elevations_request_url(gps_points)
        result = self._make_request(url)
        return result

    def get_place(self, place: str) -> Dict:
        url = self._format_places_request_url(place)
        result = self._make_request(url)
        return result

    def _format_direction_request_url(self, origin: GPSPoint, destination: GPSPoint):
        origin_param = "origin={},{}".format(*origin)
        destination_param = "destination={},{}".format(*destination)
        params = self._format_params(origin_param, destination_param)
        return self._format_api_url(GOOGLE_MAPS_DIRECTION_API_URL, params)

    def _format_elevations_request_url(self, gps_points) -> str:
        locations = "|".join(["{},{}".format(*point) for point in gps_points])
        params = self._format_params(f"locations={locations}")
        return self._format_api_url(GOOGLE_MAPS_ELEVATION_API_URL, params)

    def _format_places_request_url(self, place) -> str:
        place_param = "input={}".format(place)
        input_type = "inputtype={}".format(GOOGLE_MAPS_PLACE_API_REQUEST_TYPE)
        other_fields = "fields={}".format("geometry")
        params = self._format_params(place_param, input_type, other_fields)
        return self._format_api_url(GOOGLE_MAPS_PLACE_API_URL, params)

    def _make_request(self, url: str) -> Dict:
        self.log.debug(f"Making request to url {url}")
        result = requests.get(url).json()
        return result

    @staticmethod
    def _format_api_url(base_url: str, params: str) -> str:
        return base_url + FORMAT + "?" + params

    @staticmethod
    def _format_params(*args):
        key = f"key={app_config.GOOGLE_MAPS_KEY}"
        return PARAM_SEP.join(args) + PARAM_SEP + key
