import psycopg2
import os.path
import csv

def get_conn():
    conn = psycopg2.connect(
        host="db",
        database="ips",
        user="postgres",
        password="root")

    cur = conn.cursor()

    return conn, cur

def drop_tables(cur):
    cur.execute("DROP TABLE IF EXISTS ipv4 CASCADE")
    cur.execute("DROP TABLE IF EXISTS ipv6 CASCADE")

def create_tables(cur):
    cur.execute("""
        CREATE TABLE ipv4 (
            id SERIAL PRIMARY KEY,
            cidr CIDR NOT NULL,
            latitude TEXT NOT NULL,
            longitude TEXT NOT NULL
        )"""
    )
    cur.execute("CREATE INDEX ON ipv4 (cidr)")

    cur.execute("""
        CREATE TABLE ipv6 ( 
            LIKE ipv4 
            INCLUDING DEFAULTS 
            INCLUDING CONSTRAINTS 
            INCLUDING INDEXES
        )"""
    )


def load_data(cur):
    ipv4_path = os.path.join("geolite", "GeoLite2-City-Blocks-IPv4.csv")
    ipv6_path = os.path.join("geolite", "GeoLite2-City-Blocks-IPv6.csv")
    
    load_csv_data(cur, ipv4_path, "ipv4")
    load_csv_data(cur, ipv6_path, "ipv6")

def load_csv_data(cur, filepath, tablename):

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
            sql = "INSERT INTO " + tablename + " (cidr, latitude, longitude)" + \
            """
                VALUES (%s, %s, %s)
                RETURNING id
            """

            cur.execute(sql, (network, latitude, longitude))
            _id = cur.fetchone()[0]

            print(_id)

            if rows >= max_rows:
                break


def close_conn(conn, cur):
    cur.close()
    conn.commit()

def main():
    conn, cur = get_conn()
    drop_tables(cur)
    create_tables(cur)
    load_data(cur)
    close_conn(conn, cur)


if __name__ == '__main__': 
    main()
