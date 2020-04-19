from typing import List
from uuid import uuid1

from src.model.gps_location import GPSLocation
from src.model.package import Package
from src.model.package_tracking.event import Event
from src.model.package_tracking.tracking_data import TrackingData


class PackageTranslator:

    @staticmethod
    def tracking_data_to_package(tracking_data: TrackingData) -> Package:
        package_id: str = str(uuid1())
        package: Package = Package(package_id, tracking_data.carrier_name, tracking_data.is_delivered, "")
        package.gps_locations = PackageTranslator._translate_events(tracking_data.events)
        return package

    @staticmethod
    def _translate_events(events: List[Event]) -> List[GPSLocation]:
        gps_locations: List[GPSLocation] = []
        event: Event
        for event in events:
            gps_location_id: str = str(uuid1())
            gps_location = GPSLocation(gps_location_id,
                                       gps_location_id,
                                       event.latitude,
                                       event.longitude,
                                       event.occurred_at.isoformat())
            gps_locations.append(gps_location)
        return gps_locations
