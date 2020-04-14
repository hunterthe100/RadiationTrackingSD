import logging
import sqlite3
from typing import List

from src.model.gps_location import GPSLocation
from src.model.package import Package
from src.model.part import Part

SELECT_BY_ID = "SELECT {table_columns} FROM {table_name} WHERE {id_name} = ?"
SELECT_ALL = "SELECT {table_columns} FROM {table_name}"
SELECT_GPS_BY_ID = SELECT_BY_ID.format(table_columns="GPSCoordID, PackageID, GPSCoord, TimeStamp",
                                       table_name="GPSLocations",
                                       id_name="GPSCoordID")
SELECT_ALL_GPS = SELECT_BY_ID.format(table_columns="GPSCoordID, PackageID, GPSCoord, TimeStamp",
                                     table_name="GPSLocations")


class DataAccessObjectSQLite:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self._connection = sqlite3.connect("package.sqlite")

    def save_package(self, package: Package):
        pass

    def save_part(self, part: Part):
        pass

    def save_gps_location(self, gps_location: GPSLocation):
        pass

    def load_package(self, package_id: str) -> Package:
        pass

    def load_part(self, part_id: str) -> Part:
        pass

    def load_all_gps_locations(self) -> List[GPSLocation]:
        self.log.debug("Loading ALL GPSLocations")
        with CursorContext(self._connection) as cursor:
            cursor.execute(SELECT_ALL_GPS)
            self.log.debug("Constructing GPSLocations collection")
            return [GPSLocation(raw) for raw in cursor.fetchall()]

    def load_gps_location(self, gps_location_id: str) -> GPSLocation:
        self.log.debug(f"Loading GPSLocation with ID: {gps_location_id}")
        with CursorContext(self._connection) as cursor:
            cursor.execute(SELECT_GPS_BY_ID, [gps_location_id])
            raw = cursor.fetchone()
        return GPSLocation(raw)

    def find_gps_locations_by_package_id(self, package_id: str) -> List[GPSLocation]:
        pass

    def find_parts_by_package_id(self, package_id) -> List[Part]:
        pass


class CursorContext:
    def __init__(self, connection: sqlite3.Connection):
        self.cursor: sqlite3.Cursor = connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
