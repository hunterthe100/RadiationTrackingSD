import logging
from typing import Dict, Tuple

import requests

import app_config
from src.model.gps_tracking.road_data import RoadData

GOOGLE_MAPS_API_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/"
OUTPUT_FORMAT = "json"
ORIGIN = "origin={},{}"
DESTINATION = "destination={},{}"
KEY = "key={}"
SEP = "&"


class DataAccessObjectRoadDistance:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_maps_distance(self, origin: Tuple[float, float], destination: Tuple[float, float]) -> RoadData:
        self.log.debug("Accessing Google Directions API")

        params = SEP.join(
            [ORIGIN.format(*origin), DESTINATION.format(*destination), KEY.format(app_config.GOOGLE_MAPS_KEY)])

        url = GOOGLE_MAPS_API_DIRECTIONS_URL + OUTPUT_FORMAT + "?" + params

        response: requests.Response = requests.get(url)
        response_json: Dict = response.json()

        road_data: RoadData = RoadData(response_json)

        return road_data
