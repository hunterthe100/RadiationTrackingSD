import logging
from datetime import datetime

import requests

from src.model.gps_location import GPSPoint3D
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
        self.radiation_api_caller = RadiationAPICaller()

    def get_radiation(self, gps_point: GPSPoint3D, time: datetime, particle="total"):
        self.log.debug("Accessing Amentum Radiation API")
        response_json = self.radiation_api_caller.get_radiation_data(gps_point, time, particle)
        radiation_data = RadiationData(response_json)
        return radiation_data


class RadiationAPICaller:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_radiation_data(self, gps_point: GPSPoint3D, time: datetime, particle: str = "total"):
        year = time.year
        month = time.month
        day = time.day

        latitude, longitude, altitude = gps_point
        altitude_km = altitude / 1000

        params = self._format_params(ALTITUDE.format(altitude_km), LATITUDE.format(latitude), LONGITUDE.format(longitude),
                                     YEAR.format(year), MONTH.format(month), DAY.format(day), PARTICLE.format(particle))

        url = self._format_url(params)

        self.log.debug(f"Calling {url}")
        response: requests.Response = requests.get(url)
        return response.json()

    @staticmethod
    def _format_params(*args) -> str:
        return SEP.join(args)

    @staticmethod
    def _format_url(params: str):
        return ALTITUDE_API_URL + "?" + params
