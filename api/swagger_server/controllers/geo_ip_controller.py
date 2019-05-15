import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util


def get_coords(ip):  # noqa: E501
    """

     # noqa: E501

    :param ip: IPv4 or IPv6 address
    :type ip: str

    :rtype: InlineResponse200
    """
    return 'do some magic!'
