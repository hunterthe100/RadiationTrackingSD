import sqlite3
import app_config

CREATE_TABLE_PACKAGES = "CREATE TABLE Packages " \
                        "(PackageID TEXT, " \
                        "TrackingNumber TEXT, " \
                        "PackageCarrier TEXT, " \
                        "Delivered INTEGER, " \
                        "PackageRadiation TEXT)"

CREATE_TABLE_PARTS = "CREATE TABLE Parts " \
                     "(PartID TEXT, " \
                     "PartName TEXT, " \
                     "PartRadiation REAL)"

CRATE_TABLE_PACKAGE_PART_MAP = "CREATE TABLE PackagePartMap " \
                               "(PackageID TEXT, PartID TEXT)"


def database_setup(connection):
    cursor = connection.cursor()
    cursor.execute(CREATE_TABLE_PACKAGES)
    cursor.execute(CREATE_TABLE_PARTS)
    cursor.close()


def main():
    connection = sqlite3.connect(app_config.DATABASE_PATH)
    try:
        database_setup(connection)
    finally:
        connection.close()


if __name__ == '__main__':
    main()
