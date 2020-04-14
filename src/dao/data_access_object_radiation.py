import logging
import requests


class DataAccessObjectRadiation:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def get_radiation(self, gps_point):
        pass
