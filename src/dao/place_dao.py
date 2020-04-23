from typing import Dict, List

from src.clients.google_api_caller import GoogleAPICaller
from src.model.gps_location import GPSPoint


class PlacesDAO:
    def __init__(self):
        self.google_api_caller: GoogleAPICaller = GoogleAPICaller()

    # Return a GPSPoint object of the most likely candidate matching the place string
    def get_place(self, place: str) -> GPSPoint:
        place_json: Dict = self.google_api_caller.get_place(place)
        candidates: List = place_json["candidates"]
        best_candidate: Dict = candidates[0]
        loc = best_candidate["geometry"]["location"]
        return GPSPoint(loc['lat'], loc['lng'])
