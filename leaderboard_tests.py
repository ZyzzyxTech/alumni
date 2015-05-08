
import unittest

from api_requests import request_user_data
from api_requests import UserRequestException


class ApiRequestsTests(unittest.TestCase):
    __INVALID_USERNAME = "5"

    def test_an_invalid_username_raises_an_exception(self):
        with self.assertRaises(UserRequestException):
            request_user_data( self.__INVALID_USERNAME)
            
    def test_an_invalid_username_should_mention_a_data_issue(self):
        try:
            request_user_data(self.__INVALID_USERNAME)
        except UserRequestException as e:
            self.assertEqual(e.reason, "Recieved invalid data from profile.")
        else:
            self.assertTrue(False)