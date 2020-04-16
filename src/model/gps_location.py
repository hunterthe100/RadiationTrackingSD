class GPSLocation:
    def __init__(self,
                 gps_coord_id: str,
                 package_id: str,
                 latitude: float,
                 longitude: float,
                 time_stamp: str):
        self.gps_coord_id: str = gps_coord_id
        self.package_id: str = package_id
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.time_stamp: str = time_stamp
