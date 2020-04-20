import logging


class EnhancedGPSPoint:
    def __init__(self, latitude, longitude, altitude):
        self.log = logging.getLogger(self.__class__.__name__)
        self.lat = latitude
        self.long = longitude
        self.alt = altitude

    @property
    def latitude(self):
        return self.lat

    @property
    def longitude(self):
        return self.long

    @property
    def altitude(self):
        return self.alt
