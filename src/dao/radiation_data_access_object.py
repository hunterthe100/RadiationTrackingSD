import logging
from datetime import datetime
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


class RadiationDAO:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_radiation(self, enhanced_gps_point: EnhancedGPSPoint, time: datetime, particle="total"):
        self.log.debug("Accessing Amentum Radiation API")
        year = time.year
        month = time.month
        day = time.day

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
