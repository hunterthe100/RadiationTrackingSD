import logging


from src.clients.google_api_caller import GoogleAPICaller
from src.dao.route_data_access_object import RouteDAO
from src.dao.tracking_data_dao import TrackingDataDAO
from src.tracking_data_translator import TrackingDataTranslator


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")



def main():
    origin = (30.1356, -97.6761)
    destination = (35.0048, -89.937)

    carrier_code = "fedex"
    tracking_number = "120667023892"

    # route_dao = RouteDAO()
    # route = route_dao.get_route(origin, destination)
    # print(route.gps_points)
    # for gps in route.gps_points:
    #     print(gps)
    # print(route.elevations)
    # print(route.total_distance)
    # print(route.total_duration)

    ship_dao = TrackingDataDAO()
    ship_data = ship_dao.get_tracking_data(carrier_code, tracking_number)

    translation_test = TrackingDataTranslator()
    translation_route = translation_test.tracking_data_to_route(ship_data)

    print(translation_route.elevations)

    # google_dao = GoogleAPICaller()
    # print(google_dao.get_place("Austin, TX"))


if __name__ == '__main__':
    config_logging()
    main()
