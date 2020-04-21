import logging

from src.dao.data_access_object_route import DataAccessObjectRoute


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    origin = (30.1356, -97.6761)
    destination = (35.0048, -89.937)

    carrier_code = "fedex"
    tracking_number = "120667023892"

    route_dao = DataAccessObjectRoute()
    route = route_dao.get_route(origin, destination)
    print(route.gps_points)
    print(route.elevations)
    print(route.total_distance)
    print(route.total_duration)


if __name__ == '__main__':
    config_logging()
    main()
