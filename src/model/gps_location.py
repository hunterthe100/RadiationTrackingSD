from collections import namedtuple

GPSPoint = namedtuple("GPSPoint", ["Latitude", "Longitude"])
GPSPoint3D = namedtuple("GPSPoint3D", ["Latitude", "Longitude", "Altitude"])
