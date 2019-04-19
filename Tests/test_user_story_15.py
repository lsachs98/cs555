import unittest
from parse_gedcom import *


class TestUserStory15(unittest.TestCase):
    def setUp(self):
        fam = Family("F1")
        families.append(fam)

    def tearDown(self):
        families.clear()

    def test_no_children(self):
        table = []
        fewer_than_fifteen_siblings(table)
        self.assertTrue(table[0][3])

    def test_less_than_15_kids(self):
        table = []
        for i in range(14):
            get_family("F1").children.append(Individual("I{}".format(i + 1)))

        fewer_than_fifteen_siblings(table)
        self.assertTrue(table[0][3])

    def test_more_than_15_kids(self):
        table = []
        for i in range(20):
            get_family("F1").children.append(Individual("I{}".format(i + 1)))

        fewer_than_fifteen_siblings(table)
        self.assertFalse(table[0][3])

    def test_exactly_15_kids(self):
        table = []
        for i in range(15):
            get_family("F1").children.append(Individual("I{}".format(i + 1)))

        fewer_than_fifteen_siblings(table)
        self.assertFalse(table[0][3])


if __name__ == '__main__':
    unittest.main(verbosity=2)
