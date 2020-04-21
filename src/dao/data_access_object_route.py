from typing import Tuple, List, Dict

from src.dao.google_api_caller import GoogleAPICaller
from src.model.gps_location import GPSPoint, GPSPoint3D
from src.model.gps_tracking.route import Route


class DataAccessObjectRoute:
    def __init__(self):
        self.google_api_caller: GoogleAPICaller = GoogleAPICaller()

    # Return a Route object containing 2d gps points, 3d elevation data and other route data
    def get_route(self, origin: Tuple[float, float], destination: Tuple[float, float]) -> Route:
        route_json = self.google_api_caller.get_road_data(origin, destination)
        route = Route()
        route.gps_points = self._get_gps_points(route_json)
        route.elevations = self._get_elevation_data(route.gps_points)
        route.total_duration = self._get_total_duration_from_result(route_json)
        route.total_distance = self._get_total_distance_from_result(route_json)
        return route

    def _get_gps_points(self, google_route_json) -> List[Tuple[float, float]]:
        steps = self._get_steps_from_result(google_route_json)
        gps_points = []
        for step in steps:
            if not gps_points:  # Get the start location of only the first step
                loc = step['start_location']
            else:
                loc = step['end_location']
            gps_points.append(GPSPoint(loc['lat'], loc['lng']))
        return gps_points

    def _get_elevation_data(self, gps_points: List[Tuple[float, float]]):
        results = self.google_api_caller.get_elevations(gps_points)
        elevations = []
        for elev_data in results['results']:
            location = elev_data["location"]
            elevations.append(GPSPoint3D(location['lat'], location['lng'], elev_data['elevation']))
        return elevations

    @staticmethod
    def _get_steps_from_result(google_route_json: Dict) -> List[Dict]:
        route = DataAccessObjectRoute._get_route_from_result(google_route_json)
        steps = []
        for leg in route['legs']:
            steps.extend(leg['steps'])
        return steps

    @staticmethod
    def _get_total_distance_from_result(google_route_json: Dict) -> int:
        route = DataAccessObjectRoute._get_route_from_result(google_route_json)
        return sum([leg['distance']['value'] for leg in route['legs']])

    @staticmethod
    def _get_total_duration_from_result(google_route_json: Dict) -> int:
        route = DataAccessObjectRoute._get_route_from_result(google_route_json)
        return sum([leg['duration']['value'] for leg in route['legs']])

    @staticmethod
    def _get_route_from_result(google_route_json: Dict) -> Dict:
        return google_route_json['routes'][0]
