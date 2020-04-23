from collections import deque
from typing import Tuple, List, Dict

from src.clients.google_api_caller import GoogleAPICaller
from src.model.gps_location import GPSPoint, GPSPoint3D
from src.model.gps_tracking.route import Route, Leg, Step


class RouteDAO:
    def __init__(self):
        self.google_api_caller: GoogleAPICaller = GoogleAPICaller()

    # Return a Route object containing 2d gps points, 3d elevation data and other route data
    def get_route(self, origin: Tuple[float, float], destination: Tuple[float, float]) -> Route:
        route_json = self.google_api_caller.get_road_data(origin, destination)
        route = RouteBuilder().build(route_json)
        for leg in route.legs:
            self._convert_leg_gps_to_3d(leg)
        return route

    def _convert_leg_gps_to_3d(self, leg: Leg):
        gps_points = []
        for step in leg.steps:
            gps_points.extend(step.gps_points)
        elevation_data = deque(self._get_elevation_for_points(gps_points))
        for step in leg.steps:
            step.gps_points = (elevation_data.popleft(), elevation_data.popleft())

    def _get_elevation_for_points(self, gps_points: List[GPSPoint]) -> List[GPSPoint3D]:
        results = self.google_api_caller.get_elevations(gps_points)
        elevations = []
        for elev_data in results['results']:
            location = elev_data["location"]
            elevations.append(GPSPoint3D(location['lat'], location['lng'], elev_data['elevation']))
        return elevations

    @staticmethod
    def _get_route_from_result(google_route_json: Dict) -> Dict:
        return google_route_json['routes'][0]


class RouteBuilder:
    def __init__(self):
        self.route_json = None
        self.route: Route = None
        self._current_leg: Leg = None

    def build(self, google_route_json):
        self.route_json = google_route_json['routes'][0]
        self.route = Route()
        self._build_legs()
        return self.route

    def _build_legs(self):
        for leg_json in self.route_json['legs']:
            self._build_leg(leg_json)

    def _build_leg(self, leg_json: Dict):
        self._current_leg = Leg()
        self._build_steps(leg_json['steps'])
        self._current_leg.distance = leg_json['distance']['value']
        self._current_leg.duration = leg_json['duration']['value']
        self.route.legs.append(self._current_leg)

    def _build_steps(self, steps_json: List[Dict]):
        steps: List[Step] = []
        for step_json in steps_json:
            steps.append(self._build_step(step_json))
        self._current_leg.steps = steps

    def _build_step(self, step_json: Dict) -> Step:
        start_loc = GPSPoint(step_json['start_location']['lat'], step_json['start_location']['lng'])
        end_loc = GPSPoint(step_json['end_location']['lat'], step_json['end_location']['lng'])
        distance = step_json['distance']['value']
        duration = step_json['duration']['value']
        return Step(start_loc, end_loc, distance, duration)
