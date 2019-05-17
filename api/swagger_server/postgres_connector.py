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
        """
        Create a databse connection and cursor
        """
        self.conn = psycopg2.connect(
            host = DATABASE_HOST,
            database = DATABASE_NAME,
            user = DATABASE_USER,
            password = DATABASE_PASSWORD)

        self.cur = self.conn.cursor()

    def get_conn(self):
        """
        Create a databse connection and cursor if they don't exist, and return them
        """
        if self.conn is None: self.connect()

        return self.conn, self.cur

    def drop_tables(self):
        """
        Send drop table commands to database
        """
        self.cur.execute(f"DROP TABLE IF EXISTS {IPV4_TABLE} CASCADE")
        self.cur.execute(f"DROP TABLE IF EXISTS {IPV6_TABLE} CASCADE")

    def create_tables(self):
        """
        Send create table commands to database
        """
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
        """
        Query for an IPv4 address against the database

        Args:
            ip (str): The IPv4 address to query the database for

        Returns:
            Dictionary with latitude and longitude keys
        """
        return self.query_ip_table(ip, IPV4_TABLE)

    def query_ipv6(self, ip):
        """
        Query for an IPv6 address against the database

        Args:
            ip (str): The IPv6 address to query the database for

        Returns:
            Dictionary with latitude and longitude keys
        """
        return self.query_ip_table(ip, IPV6_TABLE)

    def query_ip_table(self, ip, tablename):
        """
        Query for an ip address against a given table in the databbse

        Args:
            ip (str): The IP address to query the database for
            tablename (str): The table to query

        Returns:
            Dictionary with latitude and longitude keys
        """

        # Build the query and fetch one result.
        # We only expect one to match
        self.cur.execute(f"SELECT latitude, longitude from {tablename} where inet %(ip)s <<= cidr", {"ip": ip})
        row = self.cur.fetchone()

        if row is None:
            return None
        
        # Package up results
        results = {
            "latitude" : row[0],
            "longitude" : row[1]
        }

        return results

    def disconnect(self):
        """
        Commit the current transaction and disconnect from the database.
        """
        self.cur.close()
        self.conn.commit()


