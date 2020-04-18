from src.dao.data_access_object_sqlite import DataAccessObjectSQLite
import logging


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    dao = DataAccessObjectSQLite()
    packages = dao.get_all_packages()
    pkg = packages[0]
    parts = dao.get_parts_for_package(pkg.package_id)
    gps_locations = dao.get_gps_locations_for_package(pkg.package_id)
    print(parts)
    print(gps_locations)


if __name__ == '__main__':
    config_logging()
    main()
