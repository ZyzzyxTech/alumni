"""
Deals with individual user statistics.
"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson,  Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["Ken W. Alger, Dan Johnson, David Dinkins, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"


class UserStats:
    def __init__(self, data):
        self.profile_name = data["profile_name"]
        self.name = data["name"]
        self.points = data["points"]
        
    def has_topic_points(self, topic):
        """
        Checks to see if the user has any points in a given topic.
        Returns False in the case of an invalid topic name.
        """
        try:
            return self.points[topic] != 0
        except KeyError:
            return False
        
    def get_topic_rank(self, topic):
        """
        Shows how a particular topic ranks among all other topics
        the user has earned atleast one point in.
        
        Raises a KeyError in the case the user has no points in
        a topic, or when the topic doesn't exist.
        """
        sorted_topics = sorted(self.points.items(), key=lambda element: element[1], reverse=True)
        
        for rank, element in enumerate(sorted_topics, 1):
            if element[0] == topic:
                return rank
                
        raise KeyError("'" + topic + "'" + " is not a valid key.")
        
    def get_topic_points(self, topic):
        """
        Gets all the points a user has gained for a particular topic.
        """
        return self.points[topic]