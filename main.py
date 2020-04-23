import logging


from src.clients.google_api_caller import GoogleAPICaller
from src.dao.route_data_access_object import RouteDAO
from src.dao.tracking_data_dao import TrackingDataDAO


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    origin = (30.1356, -97.6761)
    destination = (35.0048, -89.937)

    carrier_code = "fedex"
    tracking_number = "120667023892"

    route_dao = RouteDAO()
    route = route_dao.get_route(origin, destination)
    print(route)
    for leg in route.legs:
        print(leg)
        for step in leg.steps:
            print(step.gps_points)
            print(step.distance)
            print(step.duration)


if __name__ == '__main__':
    config_logging()
    main()
