import logging

import app_config

HEADERS = {"key": app_config.GOOGLE_MAPS_KEY}


class DataAccessObjectAltitude:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
