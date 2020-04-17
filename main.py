#from src.dao.data_access_object_sqlite import DataAccessObjectSQLite
from src.dao.data_access_object_altitude import DataAccessObjectAltitude
from src.dao.data_access_object_package_tracking import DataAccessObjectPackageTracking
import logging

from src.dao.data_access_object_radiation import DataAccessObjectRadiation
from src.dao.data_access_object_road_distance import DataAccessObjectRoadDistance


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    # Configure Logging
    config_logging()

    # Setup Data Access Object
    # d = DataAccessObjectSQLite()

    origin = "30.1356,-97.6761"
    destination = "35.0048,-89.937"

    rd = DataAccessObjectRoadDistance()
    # road_distance_test = rd.get_maps_distance(origin, destination)

    # alt = DataAccessObjectAltitude()
    # elevation_test = alt.get_altitude(origin)
    # print(elevation_test)

    rad = DataAccessObjectRadiation()
    radiation_test = rad.get_radiation()
    print(radiation_test.radiation)


if __name__ == '__main__':
    main()
