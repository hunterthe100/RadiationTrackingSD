import logging
import sqlite3
from typing import Tuple, Dict, Type, Union

import app_config
from src.model.package import Package
from src.model.part import Part


class AttrMap:
    table_name: str = ""
    id_field: str = ""
    attr_map: Dict[str, str] = {}

    def __getitem__(self, item):
        return self.attr_map[item]


class PackageAttrMap(AttrMap):
    table_name = "Packages"
    id_field = "PackageID"
    attr_map = {"PackageID": "package_id",
                "TrackingNumber": "tracking_number",
                "PackageCarrier": "carrier_code",
                "Delivered": "delivered",
                "PackageRadiation": "package_radiation"}


class PartAttrMap(AttrMap):
    table_name = "Parts"
    id_field = "PartID"
    attr_map = {"PartID": "part_id",
                "PartName": "part_name",
                "PartRadiation": "part_radiation"}


ATTR_MAPS = {Package: PackageAttrMap,
             Part: PartAttrMap}

SELECT_BY = "SELECT {table_columns} FROM {table_name} WHERE {id_name} = ?"
SELECT_ALL = "SELECT {table_columns} FROM {table_name}"
UPDATE = "UPDATE {table_name} SET {set_statement} WHERE {id_name} = ?"
INSERT = "INSERT INTO {table_name} ({table_columns}) VALUES ({values})"
DELETE = "DELETE FROM {table_name} WHERE {id_name} = ?"


class SQLiteCaller:
    def __init__(self, database_path: str):
        self.log = logging.getLogger(self.__class__.__name__)
        self.database_path: str = database_path
        self._connection = sqlite3.connect(app_config.DATABASE_PATH)

    def insert(self, obj: Union[Package, Part]):
        self._insert(obj, ATTR_MAPS[type(obj)])

    def _insert(self, obj, attr_map_cls: Type[AttrMap]):
        attr_map = attr_map_cls()
        attrs = {attr_name: getattr(obj, attr_map[attr_name]) for attr_name in attr_map.attr_map}
        columns = []
        values = []
        for column, val in attrs.items():
            columns.append(column)
            values.append(val)
        value_placeholder = ','.join(["?"] * len(values))
        sql_cmd = INSERT.format(table_name=attr_map.table_name,
                                table_columns=",".join(columns),
                                values=value_placeholder)
        with CursorContext(self._connection) as cursor:
            cursor.execute(sql_cmd, tuple(values))

    def select(self, obj_cls: Type[Union[Package, Part]], obj_id: str):
        return self._select(obj_cls, obj_id, ATTR_MAPS[obj_cls])

    def _select(self, obj_cls: Type, obj_id: str, attr_map_cls: Type[AttrMap]):
        attr_map = attr_map_cls()
        column_names = attr_map.attr_map.keys()
        sql_cmd = SELECT_BY.format(table_name=attr_map.table_name,
                                   table_columns=",".join(column_names),
                                   id_name=attr_map.id_field)
        with CursorContext(self._connection) as cursor:
            cursor.execute(sql_cmd, (obj_id,))
            values = cursor.fetchone()
        if not values:
            raise ValueError(f"Could not locate {obj_cls} in table {attr_map.table_name} with id {obj_id}")
        obj = obj_cls()
        for val, column in zip(values, column_names):
            setattr(obj, attr_map[column], val)
        return obj

    def update(self, obj: Union[Package, Part]):
        self._update(obj, ATTR_MAPS[type(obj)])

    def _update(self, obj, attr_map_cls: Type[AttrMap]):
        attr_map = attr_map_cls()

        value_placeholders = []
        columns = []
        for column in attr_map.attr_map:
            columns.append(column)
            value_placeholders.append(f"{column} = ?")

        values = [getattr(obj, attr_map[column]) for column in columns]
        values.append(getattr(obj, attr_map[attr_map.id_field]))
        sql_cmd = UPDATE.format(table_name=attr_map.table_name,
                                set_statement=", ".join(value_placeholders),
                                id_name=attr_map.id_field)

        with CursorContext(self._connection) as cursor:
            cursor.execute(sql_cmd, tuple(values))

    def delete(self, obj: Union[Package, Part]):
        self._delete(obj, ATTR_MAPS[type(obj)])

    def _delete(self, obj, attr_map_cls: Type):
        attr_map = attr_map_cls()
        sql_cmd = DELETE.format(table_name=attr_map.table_name,
                                id_name=attr_map.id_field)
        with CursorContext(self._connection) as cursor:
            cursor.execute(sql_cmd, (getattr(obj, attr_map[attr_map.id_field])))


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
        self.log.debug(f"Executing {sql_cmd} with values {values}")
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
