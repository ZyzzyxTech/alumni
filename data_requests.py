"""Handles data requests to server."""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["Ken W. Alger, Dan Johnson, David Dinkins, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

import requests

def request_user_data(username):
    """Get the JSON data as a dict for a Treehouse student."""
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