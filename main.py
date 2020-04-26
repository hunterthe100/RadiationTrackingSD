import logging
from time import time

from src.package_radiation_calculator import PackageRadiationCalculator


def config_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")


# TODO put logic for input into SQL database
def input_data(input_file: str):
    with open(input_file) as packages:
        package_string = packages.readlines()

        for thing in package_string:
            carrier_code, tracking_number, *parts = thing.split(" ")
            # logic to input into SQL


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
