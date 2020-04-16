from collections import namedtuple
from datetime import datetime
from typing import Tuple, NamedTuple, Optional


class Event:
    EventCoordinate: NamedTuple = namedtuple("EventCoordinate", ["Latitude", "Longitude"])

    def __init__(self,
                 occurred_at: str,
                 carrier_occurred_at: str,
                 description: str,
                 city_locality: str,
                 state_province: str,
                 postal_code: str,
                 country_code: str,
                 company_name: str,
                 signer: str,
                 event_code: str,
                 latitude: float,
                 longitude: float):
        self._occurred_at: str = occurred_at
        self._carrier_occurred_at: str = carrier_occurred_at
        self.description: str = description
        self.city_locality: str = city_locality
        self.state_province: str = state_province
        self.postal_code: str = postal_code
        self.country_code: str = country_code
        self.company_name: str = company_name
        self.signer: str = signer
        self.event_code: str = event_code
        self.latitude: float = latitude
        self.longitude: float = longitude

    @property
    def occurred_at(self) -> Optional[datetime]:
        return datetime.fromisoformat(self._occurred_at[:-1]) if self._carrier_occurred_at else None

    @property
    def carrier_occurred_at(self) -> Optional[datetime]:
        return datetime.fromisoformat(self._carrier_occurred_at) if self._carrier_occurred_at else None

    @property
    def coordinates(self) -> Tuple:
        return self.EventCoordinate(self.latitude, self.longitude)
