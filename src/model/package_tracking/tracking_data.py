from datetime import datetime
from typing import Optional, Dict, List

from src.model.package_tracking.event import Event


class TrackingData:
    def __init__(self,
                 carrier_code: str,
                 tracking_number: str,
                 status_code: str,
                 status_description: str,
                 carrier_status_code: str,
                 carrier_status_description: str,
                 ship_date: str,
                 actual_delivery_date: str,
                 exception_description: str,
                 events: List[Dict],
                 **kwargs):
        self.carrier_name: str = carrier_code
        self.tracking_number = tracking_number
        self.status_code = status_code
        self.status_description = status_description
        self.carrier_status_code = carrier_status_code
        self.carrier_status_description = carrier_status_description
        self._ship_date = ship_date
        self._actual_delivery_date: str = actual_delivery_date
        self.exception_description = exception_description
        self.events = [Event(**e) for e in events]

    @property
    def is_delivered(self) -> bool:
        return self.status_description == "Delivered"

    @property
    def actual_delivery_date(self) -> Optional[datetime]:
        return datetime.fromisoformat(self._actual_delivery_date[:-1]) if self._actual_delivery_date else None

    @property
    def ship_date(self) -> Optional[datetime]:
        return datetime.fromisoformat(self._ship_date[:-1]) if self._ship_date else None
