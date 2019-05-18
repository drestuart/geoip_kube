# GeoIP Kube

GeoIP Kube is a small Swagger-based API that returns approximate latitude and longitude coordinates for a given IP address. It is Docker/Kubernetes-based for easy deployment and scalability.

## Deployment


## Testing

With just one endpoint and a few error conditions, manual testing using cURL or the Swagger UI is relatively simple.

A valid cURL request that returns data will look like this:

    $ curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=1.0.1.66'
    {
      "latitude": "24.4798",
      "longitude": "118.0819"
    }

We expect a valid response (code 200) for the following requests:

    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=1.0.1.66'
    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=223.255.255.75'
    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=9c:1e::95:69:9d:41'
    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=2001:200:100::'
    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=2c0f:fff0::'
    
There are two error conditions to test, for a malformed IP address (response code 400) and for an address not found (404). For the 404 error condition do:

    $ curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=255.255.255.255'
    "IP address not found"

For the 400 error condition the expected response body is `"Invalid ip address"`. It can be tested with some or all of the following:

    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=255.255.255.256'
    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=a.b.c.d'
    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=Definitely_not_an_ip_address'
    curl -X GET --header 'Accept: application/json' 'http://localhost/v1/getCoords?ip=2001:200:100::::'

Testing can also be done in the Swagger UI by going to http://localhost/v1/ui/#!/GeoIP/get_coords and pasting the corresponding IP address in the IP field and clicking "Try It Out!".

## Development Guide

The GeoIP Kube application is based around two docker containers, the API server and a basic Postgres database container. The Postgres container is based entirely on the official Docker Hub image, so it is completely described in `docker-compose.yml`.

For the API container, `docker-compose.yml` builds off of the Dockerfile in `api/Dockerfile`, sets some database-related environment variables, and exposes port 80 for requests. The `Dockerfile` sets up the environment to run the API server, adds the data-loading cron job which runs every seven days, and kicks off the data-loading script and the Swagger server.

The server itself is a basic flask server generated from the Swagger editor (http://editor.swagger.io). It has a number of small boilerplate files related to data mapping, but the main controller logic is in `api/swagger_server/controllers/geo_ip_controller.py`. Swagger maps the `GET getCoords` request to the `get_coords(ip)` function, which validates the input IP, queries the database via the `PostgresConnector` class, and returns the latitude and longitude values in a JSON object.

The `PostgresConnector` class is defined in `api/swagger_server/postgres_controller.py` and abstracts out all database operations. A basic `PostgresConnector` workflow (a simplified version of `get_coords(ip)`) would look like this:

    connector = PostgresConnector()
    connector.connect()
    result = connector.query_ipv4(ip)
    connector.disconnect()
    return result
    
`PostgresConnector` has methods for creating and dropping tables, querying the IPv4 and IPv6 tables, inserting new records, and connecting and disconnecting from the database.

The data intake is handled by two scripts, `api/load_data.sh` and `api/swagger_server/load_data.py`. `load_data.sh` is responsible for fetching the GeoLite2 data tables from MaxMind, arranging the files, and calling `load_data.py`, and is invoked on container build and weekly by the cron job mentioned above. 

`load_data.py` creates the database tables and parses two files out of the MaxMind data, `GeoLite2-City-Blocks-IPv4.csv` and `GeoLite2-City-Blocks-IPv6.csv`, and inserts the CIDR, latitude, and longitude data into the database. It can be run by itself to refresh the database without pulling down the MaxMind data again.


## Acknowledgements

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
