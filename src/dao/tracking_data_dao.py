import logging
from typing import Dict

from src.clients.ship_engine_caller import ShipEngineCaller
from src.model.package_tracking.tracking_data import TrackingData


class TrackingDataDAO:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.ship_engine_caller = ShipEngineCaller()

    def get_tracking_data(self, carrier_code: str, tracking_number: str) -> TrackingData:
        self.log.debug(f"Accessing ShipEngine API "
                       f"| Carrier code: {carrier_code} and Tracking number: {tracking_number}")

        response_json: Dict = self.ship_engine_caller.get_tracking_data(carrier_code, tracking_number)
        tracking_data = TrackingData(carrier_code, **response_json)

        return tracking_data
