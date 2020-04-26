import logging
from typing import List

import app_config
from src.clients.sqlite_caller import SQLiteCaller
from src.model.package import Package
from src.model.part import Part


class PackageDAO:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.sql_client = SQLiteCaller(app_config.DATABASE_PATH)

    def get_package(self, package_id: str) -> Package:
        package: Package = self.sql_client.select(Package, package_id)
        package.parts = self.get_parts_for_package(package)
        return package

    def get_part(self, part_id: str) -> Part:
        part: Part = self.sql_client.select(Part, part_id)
        part.packages = self.get_packages_for_part(part)
        return part

    def save(self, obj):
        if self.sql_client.exists(obj):
            self.sql_client.update(obj)
        else:
            self.sql_client.insert(obj)
        if isinstance(obj, Package):
            relation_objs = obj.parts
        else:
            relation_objs = obj.pacakges
        for rel_obj in relation_objs:
            if self.sql_client.exists(rel_obj):
                self.sql_client.update(rel_obj)
            else:
                self.sql_client.insert(rel_obj)

    def create_mapping(self, package: Package, part: Part):
        if not self.sql_client.mapping_exists(package, part):
            self.sql_client.create_mapping(package, part)

    def get_parts_for_package(self, package: Package) -> List[Part]:
        return self.sql_client.select_by_mapping(Part, "package_id", package.package_id)

    def get_packages_for_part(self, part: Part) -> List[Package]:
        return self.sql_client.select_by_mapping(Package, "part_id", part.part_id)

    def get_all_parts(self) -> List[Part]:
        return self.sql_client.select_all(Part)

    def get_all_packages(self) -> List[Package]:
        return self.sql_client.select_all(Package)
