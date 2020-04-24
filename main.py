import logging
from datetime import datetime
from time import time

from src.clients.google_api_caller import GoogleAPICaller
from src.dao.radiation_data_access_object import RadiationDAO
from src.dao.route_data_access_object import RouteDAO
from src.dao.tracking_data_dao import TrackingDataDAO
from src.model.gps_location import GPSPoint
from src.package_radiation_calculator import PackageRadiationCalculator


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():

    # origin = GPSPoint(30.1356, -97.6761)
    # destination = GPSPoint(45.6827443, 8.7068019)
    #
    # a = RouteDAO()
    # a.get_route(origin, destination)

    start = time()

    carrier_code = "fedex"
    tracking_number = "120667023892"

    rad_calc = PackageRadiationCalculator()
    radiation = rad_calc.get_package_radiation(carrier_code, tracking_number)
    print(radiation, "uSv")

    end = time()

    print(end-start, "seconds")


    # rad_dao = RadiationDAO()
    # radiation = rad_dao.get_radiation(origin, datetime.now())
    # print(radiation)


if __name__ == '__main__':
    config_logging()
    main()
