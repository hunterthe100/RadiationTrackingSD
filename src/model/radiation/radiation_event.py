from datetime import datetime, timedelta

from src.model.gps_location import GPSPoint3D
from src.model.radiation.radiation_data import RadiationData


class RadiationEvent:
    def __init__(self):
        self.start_location: GPSPoint3D = None
        self.end_location: GPSPoint3D = None
        self.time_stamp: datetime = None
        self.radiation_data: RadiationData = None
        self.duration: timedelta = None
