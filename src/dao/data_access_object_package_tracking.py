import logging
from typing import Dict

import requests

import app_config
from src.model.package_tracking.tracking_data import TrackingData


SHIP_ENGINE_URL = "https://api.shipengine.com"
TRACKING_ENDPOINT = "/v1/tracking"
HEADERS = {"API-Key": app_config.SHIP_ENGINE_API_KEY}


class DataAccessObjectPackageTracking:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_tracking_data(self, carrier_code: str, tracking_number: str) -> TrackingData:
        self.log.debug(f"Accessing ShipEngine API "
                       f"| Carrier code: {carrier_code} and Tracking number: {tracking_number}")

        url = SHIP_ENGINE_URL + TRACKING_ENDPOINT
        params = {"carrier_code": carrier_code, "tracking_number": tracking_number}

        response: requests.Response = requests.get(url, headers=HEADERS, params=params)
        response_json: Dict = response.json()

        tracking_data = TrackingData(**response_json)

        return tracking_data
