from src.model.gps_location import GPSLocation
from src.model.package import Package
from src.dao.data_access_object_sqlite import DataAccessObjectSQLite
from src.model.part import Part

PACKAGES = [
    Package("f8673de4-7f97-11ea-9ae9-04d9f5633a79",
            "DeepSpace9Deliveries",
            1,
            "TestRadiation"),
    Package("11aab258-7f98-11ea-bfae-04d9f5633a79",
            "Brother'sMoghShipping",
            0,
            "TestRadiation"),
]
PARTS = [
    Part("7cba5b36-7f98-11ea-9894-04d9f5633a79",
         "Self Sealing Stem Bolt",
         "f8673de4-7f97-11ea-9ae9-04d9f5633a79",
         "TestRadiation"),
    Part("9c9307a6-7f98-11ea-a88f-04d9f5633a79",
         "Tribble",
         "f8673de4-7f97-11ea-9ae9-04d9f5633a79",
         "A lot"),
    Part("b903cad2-7f98-11ea-8093-04d9f5633a79",
         "Blood Wine",
         "11aab258-7f98-11ea-bfae-04d9f5633a79",
         "Some")
]

GPS_LOCATIONS = [
    GPSLocation("d8fec336-7f98-11ea-89b7-04d9f5633a79",
                "f8673de4-7f97-11ea-9ae9-04d9f5633a79",
                218.18,
                12.96,
                "2020-04-15 21:15:56.534556"),
    GPSLocation("03e27ca8-7f99-11ea-91ce-04d9f5633a79",
                "f8673de4-7f97-11ea-9ae9-04d9f5633a79",
                118.18,
                102.96,
                "2020-04-15 21:16:26.692573"),
    GPSLocation("145157d8-7f99-11ea-acbf-04d9f5633a79",
                "11aab258-7f98-11ea-bfae-04d9f5633a79",
                54.18,
                123.96,
                "2020-04-15 21:16:26.692573"),
]


def insert_test_data():
    dao = DataAccessObjectSQLite()
    create_packages(dao)
    create_parts(dao)
    create_gps_locations(dao)


def create_packages(dao):
    for package in PACKAGES:
        dao.save_package(package)


def create_parts(dao):
    for part in PARTS:
        dao.save_part(part)


def create_gps_locations(dao):
    for gps_loc in GPS_LOCATIONS:
        dao.save_gps_location(gps_loc)


def main():
    insert_test_data()


if __name__ == '__main__':
    main()
