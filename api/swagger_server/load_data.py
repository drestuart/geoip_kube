import os.path
import csv

from postgres_connector import PostgresConnector

try:
    from .geoip_config import *
except ImportError:
    from geoip_config import *

class DataLoader(object):

    def load_data(self, cur):
        ipv4_path = os.path.join("geolite", "GeoLite2-City-Blocks-IPv4.csv")
        ipv6_path = os.path.join("geolite", "GeoLite2-City-Blocks-IPv6.csv")
        
        self.load_csv_data(ipv4_path, IPV4_TABLE, cur)
        self.load_csv_data(ipv6_path, IPV6_TABLE, cur)

    def load_csv_data(self, filepath, tablename, cur):

        max_rows = 1000

        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rows = 0

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

                # Insert data
                sql = f"""
                    INSERT INTO {tablename} (cidr, latitude, longitude)
                    VALUES (%(network)s, %(latitude)s, %(longitude)s)
                    RETURNING id
                """

                cur.execute(sql, {
                    "network" : network, 
                    "latitude" : latitude, 
                    "longitude" : longitude
                })
                _id = cur.fetchone()[0]

                print(_id)

                if rows >= max_rows:
                    break

def main():
    dl = DataLoader()
    connector = PostgresConnector()
    connector.connect()
    conn, cur = connector.get_conn()
    connector.drop_tables()
    connector.create_tables()
    dl.load_data(cur)
    rec = connector.query_ipv4('1.0.1.66')
    print(rec)
    rec = connector.query_ipv6('9c:1e::95:69:9d:41')
    print(rec)
    connector.disconnect()

if __name__ == '__main__': 
    main()

