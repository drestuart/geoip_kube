import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util

from ..postgres_connector import PostgresConnector


def get_coords(ip):
    """
    :param ip: IPv4 or IPv6 address
    :type ip: str

    :rtype: InlineResponse200
    """
    connector = PostgresConnector()
    connector.connect()
    result = connector.query_ipv4(ip)
    connector.disconnect()

    return result
