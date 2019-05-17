import connexion
import six
import iptools

from swagger_server import util

from ..postgres_connector import PostgresConnector


def get_coords(ip):
    """
    Controller method for the IP -> coordinates query.

    Args:
        ip (str): The IP address to query the database for

    Returns:
        200: Dictionary with latitude and longitude keys
        400: Invalid IP address
        404: IP address not found
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

    # IP address not found
    if result is None:
        return "IP address not found", 404

    connector.disconnect()
    return result
