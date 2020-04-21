from src.dao.google_api_caller import GoogleAPICaller
from src.model.gps_tracking.route import Route
from src.model.package_tracking.tracking_data import TrackingData


class TrackingDataTranslator:
    def __init__(self):
        self.google_api_caller: GoogleAPICaller = GoogleAPICaller()

    def tracking_data_to_route(self, tracking_data: TrackingData) -> Route:
        valid_events = []
        for event in tracking_data.events:
            if event.latitude and event.longitude:
                valid_events.append(event)

        route = Route()
        route.gps_points = [event.gps_point for event in valid_events]
        route.elevations = self.google_api_caller.get_elevations(route.gps_points)
        return route
