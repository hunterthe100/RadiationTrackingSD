from collections import namedtuple


class GPSLocation:
    def __init__(self,
                 gps_coord_id: str,
                 package_id: str,
                 latitude: float,
                 longitude: float,
                 altitude: float,
                 time_stamp: str):
        self.gps_coord_id: str = gps_coord_id
        self.package_id: str = package_id
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.altitude: float = altitude
        self.time_stamp: str = time_stamp

    @property
    def gps_point(self):
        return GPSPoint(self.latitude, self.longitude)

    @property
    def gps_3d_point(self):
        return GPSPoint3D(self.latitude, self.longitude, self.altitude)


GPSPoint = namedtuple("GPSPoint", ["Latitude", "Longitude"])
GPSPoint3D = namedtuple("GPSPoint3D", ["Latitude", "Longitude", "Altitude"])
