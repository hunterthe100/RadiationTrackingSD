import logging
import requests
import app_config


class DataAccessObjectPackageTracking:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_tracking_data(self, carrier_code, tracking_number):
        self.log.debug("Accessing ShipEngine API")
        self.log.debug(F"Carrier code:{carrier_code} and Tracking number:{tracking_number}")

        full_address = "https://api.shipengine.com"
        path = "/v1/tracking"
        url = full_address + path

        headers = {"API-Key": app_config.SHIP_ENGINE_API_KEY}
        params = {"carrier_code": carrier_code, "tracking_number": tracking_number}

        r = requests.get(url, headers=headers, params=params)
        response = r.json()
        return response
