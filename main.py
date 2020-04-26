import logging
import uuid
from time import time

from src.dao.package_dao import PackageDAO
from src.model.package import Package
from src.model.part import Part
from src.package_radiation_calculator import PackageRadiationCalculator


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


# TODO put logic for input into SQL database
def input_data(input_file: str):
    with open(input_file) as f:
        package_data = f.readlines()
    package_dao = PackageDAO()
    for line in package_data:
        carrier_code, tracking_number, *part_data = line.split(" ")

        package = Package()
        package.carrier_code = carrier_code
        package.tracking_number = tracking_number
        package.package_id = str(uuid.uuid1())
        package.delivered = False
        for item in part_data:
            part = Part()
            part.part_name = item
            part.part_id = str(uuid.uuid1())
            package.parts.append(part)
        package_dao.save(package)


def main():

    start = time()

    carrier_code = "fedex"
    tracking_number = "120667023892"

    rad_calc = PackageRadiationCalculator()
    radiation = rad_calc.get_package_radiation(carrier_code, tracking_number)
    print(radiation, "uSv")

    end = time()

    print(end-start, "seconds")


if __name__ == '__main__':
    config_logging()
    main()
