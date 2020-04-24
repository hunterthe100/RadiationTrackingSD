from collections import deque
from math import radians, sin, cos, sqrt, asin
from typing import List, Dict

from src.clients.google_api_caller import GoogleAPICaller
from src.model.gps_location import GPSPoint, GPSPoint3D
from src.model.gps_tracking.route import Route, Leg, Step


class RouteDAO:
    def __init__(self):
        self.google_api_caller: GoogleAPICaller = GoogleAPICaller()

    # Return a Route object containing 2d gps points, 3d elevation data and other route data
    def get_route(self, origin: GPSPoint, destination: GPSPoint) -> Route:
        route_json = self.google_api_caller.get_road_data(origin, destination)
        status = route_json["status"]
        if status == "OK":
            route = RouteBuilder().build(route_json)
            for leg in route.legs:
                self._convert_leg_gps_to_3d(leg)
            return route
        elif status == "ZERO_RESULTS":
            return self._haversine_route_generator(origin, destination)
        else:
            raise ValueError(f"Google returned unexpected status: {status}")

    def _haversine_route_generator(self, origin: GPSPoint, destination: GPSPoint) -> Route:
        distance, time = PlanePathCalculator.get_plane_distance_and_time(origin, destination)
        route = Route()
        leg = Leg()
        leg.duration = time
        leg.distance = distance
        step = Step(GPSPoint3D(*origin, PlanePathCalculator.plane_average_altitude),
                    GPSPoint3D(*destination, PlanePathCalculator.plane_average_altitude),
                    round(distance), round(time))
        leg.steps = [step]
        route.legs.append(leg)
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


class PlanePathCalculator:
    plane_average_altitude: float = 11600.0  # Meters

    plane_average_speed: float = 267.54  # Meters

    earth_radius_km: float = 6371.0  # Kilometers

    @staticmethod
    def get_plane_distance_and_time(origin: GPSPoint, destination: GPSPoint):
        plane_distance = PlanePathCalculator._haversine(origin, destination)
        plane_time = plane_distance / PlanePathCalculator.plane_average_speed
        return plane_distance, plane_time  # Meters, seconds

    @staticmethod
    def _haversine(origin: GPSPoint, destination: GPSPoint) -> float:
        # Convert lat/lon degrees to radians
        points = [origin.Longitude, origin.Latitude, destination.Longitude, destination.Latitude]
        lon1, lat1, lon2, lat2 = map(radians, points)
        # Differences
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        # haversine formula
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = PlanePathCalculator.earth_radius_km * c
        return km * 1000.0  # Meters


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
