#from src.dao.data_access_object_sqlite import DataAccessObjectSQLite
from src.dao.data_access_object_package_tracking import DataAccessObjectPackageTracking
import logging

from src.dao.data_access_object_road_distance import DataAccessObjectRoadDistance


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    # Configure Logging
    config_logging()

    # Setup Data Access Object
    # d = DataAccessObjectSQLite()

    d = DataAccessObjectRoadDistance()
    origin = "30.1356,-97.6761"
    destination = "35.0048,-89.937"
    print(d.get_maps_distance(origin, destination))


if __name__ == '__main__':
    main()
