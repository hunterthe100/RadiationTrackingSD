from datetime import datetime, timedelta
from typing import List

from src.dao.place_dao import PlacesDAO
from src.dao.radiation_data_access_object import RadiationDAO
from src.dao.route_data_access_object import RouteDAO
from src.dao.tracking_data_dao import TrackingDataDAO
from src.model.gps_location import GPSPoint
from src.model.gps_tracking.route import Route, Leg, Step
from src.model.package_tracking.tracking_data import TrackingData
from src.model.package_tracking.tracking_event import TrackingEvent
from src.model.radiation.radiation_event import RadiationEvent


class PackageRadiationCalculator:
    def __init__(self):
        # FIXME Better to have DAO as a singleton shared across objects than a new instance for each
        self.route_dao: RouteDAO = RouteDAO()
        self.place_finder: PlacesDAO = PlacesDAO()
        self.tracking_data_dao: TrackingDataDAO = TrackingDataDAO()
        self.radiation_dao: RadiationDAO = RadiationDAO()

    def get_package_radiation(self, carrier_code: str, tracking_number: str):
        tracking_data: TrackingData = self.tracking_data_dao.get_tracking_data(carrier_code, tracking_number)
        self._normalize_tracking_events(tracking_data)

        last_event: TrackingEvent = None
        current_event: TrackingEvent
        radiation_sum = 0
        for current_event in tracking_data.tracking_events:
            if not last_event:
                last_event = current_event
                continue
            route: Route = self.route_dao.get_route(last_event.gps_point, current_event.gps_point)
            radiation_events = self._get_radiation_events(route, last_event.occurred_at, current_event.occurred_at)
            radiation_sum += self._sum_radiaiton_events(radiation_events)
        return radiation_sum

    @staticmethod
    def _sum_radiaiton_events(radiation_events: List):
        radiation_sum = 0
        for radiation_event in radiation_events:
            radiation_dose_rate = radiation_event.radiation_event.radiation_data.dose_rate
            radiation_sum += radiation_dose_rate*radiation_event.duration
        return radiation_sum

    def _get_radiation_events(self, route: Route, start_time: datetime, end_time: datetime) -> List[RadiationEvent]:
        radiation_events = []
        for leg in route.legs:
            radiation_events.extend(self._get_radiation_event_for_leg(leg, start_time, end_time))
        return radiation_events

    def _get_radiation_event_for_leg(self, leg: Leg, start_time: datetime, end_time: datetime) -> List[RadiationEvent]:
        radiation_events = []
        duration = end_time - start_time
        current_step: Step
        current_time: datetime = start_time
        for current_step in leg.steps:
            rad_event = self._create_radiation_event(current_step, current_time)
            self._populate_radiation_data(rad_event)
            radiation_events.append(rad_event)
            # Increment current time
            distance_ratio = leg.distance / current_step.distance
            step_duration = distance_ratio * duration
            rad_event.duration = step_duration
            current_time += step_duration
        return radiation_events

    # AKA Chernobyl
    def _create_radiation_event(self, step: Step, time_stamp: datetime) -> RadiationEvent:
        rad_event = RadiationEvent()
        rad_event.start_location = step.start_location
        rad_event.end_location = step.end_location
        rad_event.time_stamp = time_stamp
        return rad_event

    # Add radiation data in-place to a RadiationEvent objects
    def _populate_radiation_data(self, radiation_event: RadiationEvent):
        radiation_event.radiation_data = self.radiation_dao.get_radiation(radiation_event.start_location, radiation_event.time_stamp)

    # Modify TrackingData.tracking_events in-pace to filter unnecessary events and ensure all events have GPS locations
    # TODO: Break into multiple functions. Thicc boi
    def _normalize_tracking_events(self, tracking_data: TrackingData):
        valid_events = []
        for event in tracking_data.tracking_events:
            if event.latitude is not None and event.longitude is not None:
                valid_events.append(event)
            elif event.city_locality is not None and event.country_code is not None:
                place_string = f"{event.city_locality}, {event.country_code}"
                place: GPSPoint = self.place_finder.get_place(place_string)
                event.latitude = place.Latitude
                event.longitude = place.Longitude
                if len(valid_events) > 1:
                    if valid_events[-1].city_locality != event.city_locality:
                        valid_events.append(event)
                else:
                    valid_events.append(event)
        tracking_data.tracking_events = valid_events
