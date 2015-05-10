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

from data_requests import request_user_data
from data_requests import UserRequestException
from user_stats import UserStats


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

            
class UserStatsTests(unittest.TestCase):
    __TEST_USER_DATA = {
        "profile_name": "John",
        "name": "John Doe",
        "points": {
            "Ruby": 3000,
            "Python": 1500,
            "JavaScript": 2000,
            "Java": 1900,
            "CSS": 0
        }
    }
    
    def setUp(self):
        self.stats = UserStats(self.__TEST_USER_DATA)
    
    def test_an_invalid_topic_will_confirm_no_points(self):
        self.assertFalse(self.stats.has_topic_points("Haskell"))
        
    def test_a_valid_topic_with_no_points_is_ignored(self):
        self.assertFalse(self.stats.has_topic_points("CSS"))

    def test_ranks_are_counted_descending(self):
        self.assertEqual(1, self.stats.get_topic_rank("Ruby"))
        self.assertEqual(2, self.stats.get_topic_rank("JavaScript"))
        self.assertEqual(3, self.stats.get_topic_rank("Java"))
        self.assertEqual(4, self.stats.get_topic_rank("Python"))
        
    def test_if_no_rank_can_be_assigned_an_error_is_raised(self):
        with self.assertRaises(KeyError):
            self.stats.get_topic_rank("COBOL")