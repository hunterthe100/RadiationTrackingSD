import logging
import sqlite3
from typing import List, Tuple

import app_config
from src.model.gps_location import GPSLocation
from src.model.package import Package
from src.model.part import Part

PACKAGE_TABLE_NAME = "Packages"
PACKAGE_TABLE_COLUMNS = "PackageID, PackageCarrier, Delivered, PackageRadiation"
PACKAGE_TABLE_ID_FIELD = "PackageID"

GPS_TABLE_NAME = "GPSLocations"
GPS_TABLE_COLUMNS = "GPSCoordID, PackageID, Latitude, Longitude, TimeStamp"
GPS_TABLE_ID_FIELD = "GPSCoordID"

PART_TABLE_NAME = "Parts"
PART_TABLE_COLUMNS = "PartID, PartName, PackageID, PartRadiation"
PART_TABLE_ID_FIELD = "PartID"

SELECT_BY = "SELECT {table_columns} FROM {table_name} WHERE {id_name} = ?"
SELECT_ALL = "SELECT {table_columns} FROM {table_name}"
INSERT = "INSERT INTO {table_name} ({table_columns}) VALUES ({values})"
DELETE = "DELETE FROM {table_name} WHERE {id_name} = ?"


# TODO: Break this into SQLite caller + DAO
class SQLiteDAO:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self._connection = sqlite3.connect(app_config.DATABASE_PATH)

    def _get(self, object_class, table_name: str, table_columns: str, id_name: str, obj_id) -> List:
        self.log.debug(f"Getting {object_class} by {id_name} = {obj_id}")
        sql_cmd: str = SELECT_BY.format(table_name=table_name,
                                        table_columns=table_columns,
                                        id_name=id_name)
        with CursorContext(self._connection) as cursor:
            cursor.execute(sql_cmd, (obj_id,))
            raw = cursor.fetchall()
        return [object_class(*values) for values in raw]

    def _get_all(self, object_class, table_name: str, table_columns: str) -> List:
        self.log.debug(f"Getting all {object_class}")
        sql_cmd: str = SELECT_ALL.format(table_name=table_name,
                                         table_columns=table_columns)
        with CursorContext(self._connection) as cursor:
            cursor.execute(sql_cmd)
            return [object_class(*raw) for raw in cursor.fetchall()]

    def _save(self, table_name: str, table_columns: str, values: Tuple):
        sql_cmd: str = INSERT.format(table_name=table_name,
                                     table_columns=table_columns,
                                     values=", ".join(["?"] * len(values)))
        with CursorContext(self._connection) as cursor:
            cursor.execute(sql_cmd, values)

    def _delete(self, table_name: str, id_name: str, obj_id):
        self.log.debug(f"Deleting from {table_name} where {id_name} = {obj_id}")
        sql_cmd: str = DELETE.format(table_name=table_name,
                                     id_name=id_name)
        with CursorContext(self._connection) as cursor:
            cursor.execute(sql_cmd, obj_id)

    def save_package(self, package: Package):
        self.log.debug(f"Inserting Package with ID: {package.package_id}")
        values = (package.package_id, package.package_carrier, package.delivered, package.package_radiation)
        self._save(PACKAGE_TABLE_NAME, PACKAGE_TABLE_COLUMNS, values)
        part: Part
        for part in package.parts:
            self.save_part(part)
        for gps_location in package.gps_locations:
            self.save_gps_location(gps_location)

    def save_part(self, part: Part):
        self.log.debug(f"Inserting Part with ID: {part.part_id}")
        values = (part.part_id, part.part_name, part.package_id, part.part_radiation)
        self._save(PART_TABLE_NAME, PART_TABLE_COLUMNS, values)

    def save_gps_location(self, gps_location: GPSLocation):
        self.log.debug(f"Inserting GPSLocation with ID: {gps_location.gps_coord_id}")
        values = (gps_location.gps_coord_id, gps_location.package_id, gps_location.latitude, gps_location.longitude,
                  gps_location.time_stamp)
        self._save(GPS_TABLE_NAME, GPS_TABLE_COLUMNS, values)

    def get_package(self, package_id: str) -> Package:
        # This could be made into a single SQL operation
        package = self._get(Package, PACKAGE_TABLE_NAME, PACKAGE_TABLE_COLUMNS, PACKAGE_TABLE_ID_FIELD, package_id)[0]
        package.parts = self.get_parts_for_package(package.package_id)
        package.gps_locations = self.get_gps_locations_for_package(package_id)
        return package

    def get_all_packages(self) -> List[Package]:
        self.log.warning("This is an expensive operation and you should use `get_package` instead!")
        return self._get_all(Package, PACKAGE_TABLE_NAME, PACKAGE_TABLE_COLUMNS)

    def get_part(self, part_id: str) -> Part:
        return self._get(Part, PART_TABLE_NAME, PART_TABLE_COLUMNS, PART_TABLE_ID_FIELD, part_id)[0]

    def get_all_parts(self) -> List[Part]:
        self.log.warning("This is an expensive operation and you should use `get_part` instead!")
        return self._get_all(Part, PART_TABLE_NAME, PART_TABLE_COLUMNS)

    def get_gps_location(self, gps_location_id: str) -> GPSLocation:
        return self._get(GPSLocation, GPS_TABLE_NAME, GPS_TABLE_COLUMNS, GPS_TABLE_ID_FIELD, gps_location_id)[0]

    def get_all_gps_locations(self) -> List[GPSLocation]:
        self.log.warning("This is an expensive operation and you should use `get_gps_location` instead!")
        return self._get_all(GPSLocation, GPS_TABLE_NAME, GPS_TABLE_COLUMNS)

    def get_gps_locations_for_package(self, package_id: str) -> List[GPSLocation]:
        return self._get(GPSLocation, GPS_TABLE_NAME, GPS_TABLE_COLUMNS, PACKAGE_TABLE_ID_FIELD, package_id)

    def get_parts_for_package(self, package_id: str) -> List[Part]:
        return self._get(Part, PART_TABLE_NAME, PART_TABLE_COLUMNS, PACKAGE_TABLE_ID_FIELD, package_id)


class CursorContext:
    def __init__(self, connection: sqlite3.Connection):
        self.log = logging.getLogger(self.__class__.__name__)
        self.connection = connection
        self.cursor: sqlite3.Cursor = connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.commit()

    # Delegate attribute lookups to cursor
    def __getattr__(self, item):
        return self.cursor.__getattribute__(item)

    # Add exception logging to cursor execute method
    def execute(self, sql_cmd, values: Tuple = None):
        try:
            if values:
                return self.cursor.execute(sql_cmd, values)
            else:
                return self.cursor.execute(sql_cmd)
        except Exception as e:
            self.log.error(f"Failed to execute SQL: {sql_cmd}\nError: {e}")
            raise

    # Pass-through method call for IDE code completion
    def fetchone(self):
        return self.cursor.fetchone()

    # Pass-through method call for IDE code completion
    def fetchmany(self, size):
        return self.cursor.fetchmany(size)

    # Pass-through method call for IDE code completion
    def fetchall(self):
        return self.cursor.fetchall()
