from datetime import datetime
from typing import Optional

from src.model.gps_location import GPSPoint, GPSPoint3D


class TrackingEvent:

    def __init__(self,
                 occurred_at: str,
                 carrier_occurred_at: str,
                 description: str,
                 city_locality: str,
                 state_province: str,
                 postal_code: str,
                 country_code: str,
                 latitude: float,
                 longitude: float,
                 **kwargs):
        self._occurred_at: str = occurred_at
        self._carrier_occurred_at: str = carrier_occurred_at
        self.description: str = description
        self.city_locality: str = city_locality
        self.state_province: str = state_province
        self.postal_code: str = postal_code
        self.country_code: str = country_code
        self.latitude: float = latitude
        self.longitude: float = longitude

        self.altitude: float = None

    @property
    def occurred_at(self) -> Optional[datetime]:
        return datetime.fromisoformat(self._occurred_at[:-1]) if self._carrier_occurred_at else None

    @property
    def carrier_occurred_at(self) -> Optional[datetime]:
        return datetime.fromisoformat(self._carrier_occurred_at) if self._carrier_occurred_at else None

    @property
    def gps_point(self) -> GPSPoint:
        return GPSPoint(self.latitude, self.longitude)

    @property
    def gps_3d_point(self) -> GPSPoint3D:
        if self.altitude is None:
            raise ValueError("Altitude must be present to construct 3D GPS point")
        return GPSPoint3D(self.latitude, self.longitude, self.altitude)
