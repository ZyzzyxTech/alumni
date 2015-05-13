__author__ = 'Ken'

import unittest
import requests

from playhouse.test_utils import test_database
from playhouse.postgres_ext import PostgresqlExtDatabase

from models import Student, User

TEST_DB = PostgresqlExtDatabase(database='test', user='postgres')
TEST_DB.connect()
TEST_DB.drop_tables([Student, User])
TEST_DB.create_tables([Student, User], safe=True)

STUDENT_DATA = {
    'th_username': 'kenalger',
    'email': 'test_0@example.com',
    'first_name': 'Ken',
    'last_name': 'Alger',
    'password': 'password',
    'github_username': 'kenwalger',
    'city': 'Keizer',
    'state': 'OR',
    'country': 'USA'
}

STUDENT_LIST = ['kenalger', 'craigsdennis', 'kennethlove']


class StudentModelTestCase(unittest.TestCase):
    @staticmethod
    def create_students(count=2):
        for i in range(count):
            Student.create_student(
                username=STUDENT_LIST[i],
                user_json=requests.get("https://teamtreehouse.com/{}.json".format(STUDENT_LIST[i])).json(),
                email='test_{}@example.com'.format(i),
                first_name='John',
                last_name='Doe',
                password='password',
                github_username=STUDENT_LIST[i],
                city='Portland',
                state='OR',
                country='USA'
            )

    def test_create_student(self):
        with test_database(TEST_DB, (Student,)):
            self.create_students(),
            self.assertEqual(Student.select().count(), 2)
            self.assertNotEqual(
                Student.select().get().password, 'password'
            )

    def test_create_duplicate_student(self):
        with test_database(TEST_DB, (Student,)):
            self.create_students()
            with self.assertRaises(ValueError):
                Student.create_student(
                    username='kenalger',
                    user_json=requests.get("https://teamtreehouse.com/kenalger.json").json(),
                    email='test_0@example.com',
                    first_name='John',
                    last_name='Doe',
                    password='password',
                    github_username='kenwalger',
                    city='Portland',
                    state='OR',
                    country='USA'
                )


if __name__ == '__main__':
    unittest.main()