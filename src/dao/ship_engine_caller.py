import logging
from typing import Dict

import requests

import app_config

SHIP_ENGINE_URL = "https://api.shipengine.com"
TRACKING_ENDPOINT = "/v1/tracking"
HEADERS = {"API-Key": app_config.SHIP_ENGINE_API_KEY}


class ShipEngineCaller:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_tracking_data(self, carrier_code: str, tracking_number: str) -> Dict:
        url = SHIP_ENGINE_URL + TRACKING_ENDPOINT
        params = self._format_params(carrier_code, tracking_number)
        response: requests.Response = self._make_request(url, params)
        return response.json()

    def _make_request(self, url, params):
        self.log.debug(f"Making request to url {url} with params: {params}")
        return requests.get(url, headers=HEADERS, params=params)

    @staticmethod
    def _format_params(carrier_code: str, tracking_number: str):
        return {"carrier_code": carrier_code, "tracking_number": tracking_number}
