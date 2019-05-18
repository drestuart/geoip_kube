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



## Acknowledgements

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
