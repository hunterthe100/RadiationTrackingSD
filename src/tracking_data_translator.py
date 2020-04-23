from src.dao.place_dao import PlacesDAO
from src.dao.route_data_access_object import RouteDAO
from src.model.gps_location import GPSPoint
from src.model.gps_tracking.route import Route
from src.model.package_tracking.tracking_data import TrackingData


class TrackingDataTranslator:
    def __init__(self):
        # FIXME Better to have DAO as a singleton shared across objects than a new instance for each
        self.route_dao: RouteDAO = RouteDAO()
        self.place_finder: PlacesDAO = PlacesDAO()

    def tracking_data_to_route(self, tracking_data: TrackingData) -> Route:
        valid_events = self.valid_events_finder(tracking_data)
        route = Route()
        route.gps_points = [event.gps_point for event in valid_events]
        route.elevations = self.route_dao.get_elevation_for_points(route.gps_points)
        return route

    def valid_events_finder(selfself, tracking_data: TrackingData):
        valid_events = []
        for event in tracking_data.events:
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
        return valid_events
