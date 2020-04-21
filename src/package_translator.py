from typing import List
from uuid import uuid1

from src.dao.data_access_object_altitude import DataAccessObjectAltitude
from src.model.gps_location import GPSLocation
from src.model.package import Package
from src.model.package_tracking.event import Event
from src.model.package_tracking.tracking_data import TrackingData


class PackageTranslator:
    def __init__(self, altitude_dao: DataAccessObjectAltitude):
        self.altitude_dao: DataAccessObjectAltitude = altitude_dao

    def tracking_data_to_package(self, tracking_data: TrackingData) -> Package:
        package_id: str = str(uuid1())
        package: Package = Package(package_id, tracking_data.carrier_name, tracking_data.is_delivered, "")
        package.gps_locations = self._translate_events(tracking_data.events)
        return package

    def _translate_events(self, events: List[Event]) -> List[GPSLocation]:
        gps_locations: List[GPSLocation] = []
        gps_3d_points = self.altitude_dao.get_altitudes([event.gps_point for event in events])
        event: Event
        for event, gps_point in zip(events, gps_3d_points):
            gps_location_id: str = str(uuid1())
            gps_location = GPSLocation(gps_location_id,
                                       gps_location_id,
                                       event.latitude,
                                       event.longitude,
                                       gps_point[2],
                                       event.occurred_at.isoformat())
            gps_locations.append(gps_location)
        return gps_locations
