import logging
from typing import Dict

import requests

import app_config
from src.model.gps_tracking.enhanced_gps_point import EnhancedGPSPoint

GOOGLE_MAPS_API_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/elevation/"
OUTPUT_FORMAT = "json"
LOCATIONS = "locations={}"
KEY = "key={}"
SEP = "&"


class DataAccessObjectAltitude:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_altitude(self, gps_point):
        self.log.debug("Accessing Google Elevation API")

        params = SEP.join([LOCATIONS.format(gps_point), KEY.format(app_config.GOOGLE_MAPS_KEY)])

        url = GOOGLE_MAPS_API_DIRECTIONS_URL + OUTPUT_FORMAT + "?" + params

        response: requests.Response = requests.get(url)
        response_json: Dict = response.json()

        # tracking_data = TrackingData(**response_json)

        return response_json
