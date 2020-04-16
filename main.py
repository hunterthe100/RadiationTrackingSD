from src.dao.data_access_object_sqlite import DataAccessObjectSQLite
import logging


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    dao = DataAccessObjectSQLite()
    packages = dao.get_all_packages()
    parts = dao.get_all_parts()
    gps = dao.get_all_gps_locations()
    print(packages)
    print(parts)
    print(gps)


if __name__ == '__main__':
    config_logging()
    main()
