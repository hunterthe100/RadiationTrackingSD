import logging

from src.dao.data_access_object_package_tracking import DataAccessObjectPackageTracking
from src.model.package import Package
from src.model.package_tracking.tracking_data import TrackingData
from src.package_translator import PackageTranslator


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    dao = DataAccessObjectPackageTracking()
    carrier_code = "fedex"
    tracking_number = "120667023892"
    tracking_data: TrackingData = dao.get_tracking_data(carrier_code, tracking_number)
    package: Package = PackageTranslator.tracking_data_to_package(tracking_data)
    print(package)
    print(package.gps_locations)


if __name__ == '__main__':
    config_logging()
    main()
