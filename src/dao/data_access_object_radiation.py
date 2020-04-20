import logging
from typing import Dict

import requests

from src.model.gps_tracking.enhanced_gps_point import EnhancedGPSPoint
from src.model.radiation.radiation_data import RadiationData

ALTITUDE_API_URL = "https://cosmicrays.amentum.space/parma/ambient_dose"
ALTITUDE = "altitude={}"
LATITUDE = "latitude={}"
LONGITUDE = "longitude={}"
YEAR = "year={}"
MONTH = "month={}"
DAY = "day={}"
PARTICLE = "particle={}"

SEP = "&"


class DataAccessObjectRadiation:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_radiation(self, enhanced_gps_point: EnhancedGPSPoint, time="b", particle="total"):
        self.log.debug("Accessing Google Directions API")

        # TODO remove all of this when enhanced_gps_points and time format are known better
        year = 2019
        month = 12
        day = 1

        altitude = enhanced_gps_point.altitude
        latitude = enhanced_gps_point.latitude
        longitude = enhanced_gps_point.longitude

        params = SEP.join(
            [ALTITUDE.format(altitude), LATITUDE.format(latitude), LONGITUDE.format(longitude),
             YEAR.format(year), MONTH.format(month), DAY.format(day), PARTICLE.format(particle)])

        url = ALTITUDE_API_URL + "?" + params

        response: requests.Response = requests.get(url)
        response_json: Dict = response.json()

        radiation_data = RadiationData(response_json)

        return radiation_data
