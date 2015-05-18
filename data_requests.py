"""
Handles data requests to server.
"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["David Dinkins, Ken W. Alger, Dan Johnson, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

import requests

from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from requests.exceptions import RequestException


def request_user_data(username):
    """
    Get the JSON data as a dict for a Treehouse student.

    Args:
        username: A Treehouse user name

    Raises:
        Timeout:
        ConnectionError:
        RequestException:
        ValueError: A non-valid Treehouse username
    """
    data = None

    try:
        response = requests.get("https://teamtreehouse.com/{}.json".format(username))
        data = response.json()
    except Timeout:
        raise UserRequestException("Request timed out. Try again in a few minutes.")
    except ConnectionError:
        raise UserRequestException("Connection was refused.")
    except RequestException:
        raise UserRequestException("There was an issue communicating with the server.")
    except ValueError:
        raise UserRequestException("Received invalid data from profile.")
    else:
        return data
        
        
class UserRequestException(Exception):
    def __init__(self, reason):
        self.reason = reason
        
    def __str__(self):
        return self.reason