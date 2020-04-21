import logging

from src.dao.data_access_object_altitude import DataAccessObjectAltitude
from src.dao.data_access_object_package_tracking import DataAccessObjectPackageTracking
from src.model.package import Package
from src.model.package_tracking.tracking_data import TrackingData
from src.package_translator import PackageTranslator


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    carrier_code = "fedex"
    tracking_number = "120667023892"

    package_tracking_dao = DataAccessObjectPackageTracking()
    altitude_dao = DataAccessObjectAltitude()
    package_translator = PackageTranslator(altitude_dao)

    tracking_data: TrackingData = package_tracking_dao.get_tracking_data(carrier_code, tracking_number)
    package: Package = package_translator.tracking_data_to_package(tracking_data)

    print(package)
    print(package.gps_locations)
    for gps in package.gps_locations:
        print(gps.latitude, gps.longitude, gps.altitude)


if __name__ == '__main__':
    config_logging()
    main()
