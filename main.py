#from src.dao.data_access_object_sqlite import DataAccessObjectSQLite
from src.dao.data_access_object_package_tracking import DataAccessObjectPackageTracking
import logging


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


def main():
    # Configure Logging
    config_logging()

    # Setup Data Access Object
    # d = DataAccessObjectSQLite()
    a = DataAccessObjectPackageTracking()

    carrier_code = "fedex"
    tracking_number = "120667023892"
    response = a.get_tracking_data(carrier_code,tracking_number)

    print(response)


if __name__ == '__main__':
    main()
