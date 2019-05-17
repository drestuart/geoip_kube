import psycopg2
try:
    from .geoip_config import *
except ImportError:
    from geoip_config import *

class PostgresConnector(object):

    def __init__(self):
        self.con = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect(
            host="db",
            database="geoip",
            user="postgres",
            password="root")

        self.cur = self.conn.cursor()

    def get_conn(self):
        if self.conn is None: self.connect()

        return self.conn, self.cur

    def drop_tables(self):
        self.cur.execute(f"DROP TABLE IF EXISTS {IPV4_TABLE} CASCADE")
        self.cur.execute(f"DROP TABLE IF EXISTS {IPV6_TABLE} CASCADE")

    def create_tables(self):
        self.cur.execute(f"""
            CREATE TABLE {IPV4_TABLE} (
                id SERIAL PRIMARY KEY,
                cidr CIDR NOT NULL,
                latitude TEXT NOT NULL,
                longitude TEXT NOT NULL
            )"""
        )
        self.cur.execute(f"CREATE INDEX ON {IPV4_TABLE} (cidr)")

        self.cur.execute(f"""
            CREATE TABLE {IPV6_TABLE} ( 
                LIKE {IPV4_TABLE} 
                INCLUDING DEFAULTS 
                INCLUDING CONSTRAINTS 
                INCLUDING INDEXES
            )"""
        )

    def query_ipv4(self, ip):
        return self.query_ip_table(ip, IPV4_TABLE)

    def query_ipv6(self, ip):
        return self.query_ip_table(ip, IPV6_TABLE)

    def query_ip_table(self, ip, tablename):
        self.cur.execute(f"SELECT latitude, longitude from {tablename} where inet %(ip)s <<= cidr", {"ip": ip})

        row = self.cur.fetchone()

        if row is None:
            return None
        
        results = {
            "latitude" : row[0],
            "longitude" : row[1]
            }

        return results

    def close_conn(self, conn, cur):
        cur.close()
        conn.commit()

    def disconnect(self):
        self.close_conn(self.conn, self.cur)

