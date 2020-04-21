from src.dao.data_access_object_route import DataAccessObjectRoute
from src.model.gps_tracking.route import Route
from src.model.package_tracking.tracking_data import TrackingData


class TrackingDataTranslator:
    def __init__(self):
        # FIXME Better to have DAO as a singleton shared across objects than a new instance for each
        self.route_dao: DataAccessObjectRoute = DataAccessObjectRoute()

    def tracking_data_to_route(self, tracking_data: TrackingData) -> Route:
        valid_events = []
        for event in tracking_data.events:
            if event.latitude and event.longitude:
                valid_events.append(event)

        route = Route()
        route.gps_points = [event.gps_point for event in valid_events]
        route.elevations = self.route_dao.get_elevation_for_points(route.gps_points)
        return route
