import unittest
from parse_gedcom import *
from io import StringIO
from contextlib import redirect_stdout


class TestUserStory15(unittest.TestCase):
    def setUp(self):
        fam = Family("F1")
        families.append(fam)

    def tearDown(self):
        families.clear()

    def test_no_children(self):
        capture = StringIO()

        with redirect_stdout(capture):
            fewer_than_fifteen_siblings()

        self.assertIn("All families have less than 15 children.", capture.getvalue().strip().split("\n"))

    def test_less_than_15_kids(self):
        capture = StringIO()

        for i in range(10):
            get_family("F1").children.append(Individual("I{}".format(i+1)))

        with redirect_stdout(capture):
            fewer_than_fifteen_siblings()

        self.assertIn("All families have less than 15 children.", capture.getvalue().strip().split("\n"))

    def test_more_than_15_kids(self):
        capture = StringIO()

        for i in range(20):
            get_family("F1").children.append(Individual("I{}".format(i+1)))

        with redirect_stdout(capture):
            fewer_than_fifteen_siblings()

        self.assertIn("Some families have too many children.", capture.getvalue().strip().split("\n"))

    def test_exactly_15_kids(self):
        capture = StringIO()

        for i in range(15):
            get_family("F1").children.append(Individual("I{}".format(i+1)))

        with redirect_stdout(capture):
            fewer_than_fifteen_siblings()

        self.assertIn("Some families have too many children.", capture.getvalue().strip().split("\n"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
