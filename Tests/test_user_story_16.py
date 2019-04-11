import unittest
from parse_gedcom import *
from io import StringIO
from contextlib import redirect_stdout


class TestUserStory16(unittest.TestCase):
    def setUp(self):
        fam = Family("F1")
        families.append(fam)

    def tearDown(self):
        families.clear()


if __name__ == '__main__':
    unittest.main(verbosity=2)
