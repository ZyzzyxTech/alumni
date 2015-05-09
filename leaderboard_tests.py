"""This will create the Treehouse Leaderboard Application tests"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["Ken W. Alger, Dan Johnson, David Dinkins, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

import unittest

from api_requests import request_user_data
from api_requests import UserRequestException


class ApiRequestsTests(unittest.TestCase):
    __INVALID_USERNAME = "5"

    def test_an_invalid_username_raises_an_exception(self):
        with self.assertRaises(UserRequestException):
            request_user_data(self.__INVALID_USERNAME)
            
    def test_an_invalid_username_should_mention_a_data_issue(self):
        try:
            request_user_data(self.__INVALID_USERNAME)
        except UserRequestException as e:
            self.assertEqual(e.reason, "Recieved invalid data from profile.")
        else:
            self.assertTrue(False)


