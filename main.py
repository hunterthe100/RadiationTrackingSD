import logging
from datetime import datetime

from src.clients.google_api_caller import GoogleAPICaller
from src.dao.radiation_data_access_object import RadiationDAO
from src.dao.route_data_access_object import RouteDAO
from src.dao.tracking_data_dao import TrackingDataDAO
from src.model.gps_location import GPSPoint3D
from src.package_radiation_calculator import PackageRadiationCalculator


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    origin = (30.1356, -97.6761)
    destination = (35.0048, -89.937)

    origin = GPSPoint3D(30.1356, -97.6761, 800)

    carrier_code = "fedex"
    tracking_number = "120667023892"

    rad_calc = PackageRadiationCalculator()
    radiation = rad_calc.get_package_radiation(carrier_code, tracking_number)
    print(radiation)

    # rad_dao = RadiationDAO()
    # radiation = rad_dao.get_radiation(origin, datetime.now())
    # print(radiation)


if __name__ == '__main__':
    config_logging()
    main()
