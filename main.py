# from src.dao.data_access_object_sqlite import DataAccessObjectSQLite

import logging

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
    road_distance_test = rd.get_maps_distance(origin, destination)

    print(road_distance_test)
    print(road_distance_test.duration)
    print(road_distance_test.distance)

    # alt = DataAccessObjectAltitude()
    # elevation_test = alt.get_altitude(origin)
    # print(elevation_test)

    # rad = DataAccessObjectRadiation()
    # altitude = 155.1155700683594 / 1000
    # latitude = 30.1356
    # longitude = -97.6761
    # egps = EnhancedGPSPoint(longitude=longitude, latitude=latitude, altitude=altitude)
    # radiation_test = rad.get_radiation(egps)
    # print(radiation_test.radiation)


if __name__ == '__main__':
    config_logging()
    main()
