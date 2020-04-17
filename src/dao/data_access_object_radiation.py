import logging
from typing import Dict

import requests

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

    def get_radiation(self, enhanced_gps_point="a", time="b", particle="total"):
        self.log.debug("Accessing Google Directions API")
        alt = 155.1155700683594/1000
        latitude = 30.1356
        longitude = -97.6761
        year = 2019
        month = 12
        day = 1

        params = SEP.join(
            [ALTITUDE.format(alt), LATITUDE.format(latitude), LONGITUDE.format(longitude),
             YEAR.format(year), MONTH.format(month), DAY.format(day), PARTICLE.format(particle)])

        url = ALTITUDE_API_URL + "?" + params

        response: requests.Response = requests.get(url)
        response_json: Dict = response.json()

        radiation_data = RadiationData(response_json)

        return radiation_data
