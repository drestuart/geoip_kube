import connexion
import six
import iptools

from swagger_server import util

from ..postgres_connector import PostgresConnector


def get_coords(ip):
    """
    """
    connector = PostgresConnector()
    connector.connect()

    is_ipv4 = False
    is_ipv6 = False

    # Validate input IP
    try:
        is_ipv4 = iptools.ipv4.validate_ip(ip)
    except TypeError:
        pass

    try:
        is_ipv6 = iptools.ipv6.validate_ip(ip)
    except TypeError:
        pass

    # Route to the appropriate db query
    if is_ipv4:
        result = connector.query_ipv4(ip)
    elif is_ipv6:
        result = connector.query_ipv6(ip)
    else:
        result = "Invalid ip address", 400

    # Not found
    if result is None:
        return "IP address not found", 404

    connector.disconnect()
    return result
