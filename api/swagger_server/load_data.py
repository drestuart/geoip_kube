import os.path
import csv

from postgres_connector import PostgresConnector

try:
    from .geoip_config import *
except ImportError:
    from geoip_config import *

class DataLoader(object):

    @staticmethod
    def load_data(cur):
        """
        Load IPv4 and IPv6 files into the database

        Args:
            cur: The database cursor
        """
        ipv4_path = os.path.join("geolite", "GeoLite2-City-Blocks-IPv4.csv")
        ipv6_path = os.path.join("geolite", "GeoLite2-City-Blocks-IPv6.csv")
        
        DataLoader.load_csv_data(ipv4_path, IPV4_TABLE, cur)
        DataLoader.load_csv_data(ipv6_path, IPV6_TABLE, cur)

    @staticmethod
    def load_csv_data(filepath, tablename, cur):
        """
        Parse CSV data and load into database

        Args:
            filepath (str): The file path to load
            tablename (str): The table to insert into
            cur: The database cursor
        """

        max_rows = 10000

        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rows = 0

            # Get the header row, and find the columns we're interested in
            header_row = reader.__next__()
            network_col = header_row.index("network")
            lat_col = header_row.index("latitude")
            long_col = header_row.index("longitude")

            for row in reader:
                rows += 1

                # Extract data from columns
                network = row[network_col]
                latitude = row[lat_col]
                longitude = row[long_col]

                # Build query and insert data
                sql = f"""
                    INSERT INTO {tablename} (cidr, latitude, longitude)
                    VALUES (%(network)s, %(latitude)s, %(longitude)s)
                """

                cur.execute(sql, {
                    "network" : network, 
                    "latitude" : latitude, 
                    "longitude" : longitude
                })

                if rows % 1000 == 0:
                    print(f"Loading row {rows} into table {tablename}")

                if rows >= max_rows:
                    break

def main():
    """
    Data loading process
    """

    # Connect to database
    connector = PostgresConnector()
    connector.connect()
    conn, cur = connector.get_conn()

    # Recreate tables
    connector.drop_tables()
    connector.create_tables()

    # Load all data
    DataLoader.load_data(cur)

    # Run some test queries
    rec = connector.query_ipv4('1.0.1.66')
    print('1.0.1.66 =>', rec)
    rec = connector.query_ipv6('9c:1e::95:69:9d:41')
    print('9c:1e::95:69:9d:41 =>', rec)

    # Close db connection
    connector.disconnect()

if __name__ == '__main__': 
    main()

