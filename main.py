#from src.dao.data_access_object_sqlite import DataAccessObjectSQLite
from src.dao.data_access_object_package_tracking import DataAccessObjectPackageTracking
import logging

from src.model.package_tracking.event import Event
from src.model.package_tracking.tracking_data import TrackingData


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    # Configure Logging
    config_logging()

    # Setup Data Access Object
    # d = DataAccessObjectSQLite()
    package_tracking_dao = DataAccessObjectPackageTracking()

    carrier_code = "fedex"
    tracking_number = "120667023892"
    tracking_data: TrackingData = package_tracking_dao.get_tracking_data(carrier_code, tracking_number)

    if tracking_data.is_delivered:
        event: Event
        for event in tracking_data.events:
            print(event.coordinates)


if __name__ == '__main__':
    main()
