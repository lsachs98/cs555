import unittest
from parse_gedcom import *


class TestUserStory35(unittest.TestCase):
    def setUp(self):
        ind1 = Individual("I1")
        ind1.name = "Recent /Birth1/"
        ind1.birth = datetime.strptime("20 AUG 2018", "%d %b %Y").date()
        ind2 = Individual("I2")
        ind2.name = "Far /Birth2/"
        ind2.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        ind3 = Individual("I3")
        ind3.name = "Far /Birth3/"
        ind3.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        ind4 = Individual("I4")
        ind4.name = "Recent /Birth4/"
        ind4.birth = datetime.strptime("18 AUG 2018", "%d %b %Y").date()

        individuals.append(ind1)
        individuals.append(ind2)
        individuals.append(ind3)
        individuals.append(ind4)

    def tearDown(self):
        individuals.clear()

    def test_empty_file(self):
        individuals.clear()
        table = []
        list_recent_births(table)
        self.assertFalse(table[0][4].split()) and self.assertTrue(table[0][3])

    def test_mixed_births(self):
        table = []
        list_recent_births(table)
        self.assertCountEqual([get_individual("I1").name, get_individual("I4").name],
                              table[0][4].split("\n")) and self.assertTrue(table[0][3])

    def test_all_recent_births(self):
        get_individual("I2").birth = datetime.strptime("19 AUG 2018", "%d %b %Y").date()
        get_individual("I3").birth = datetime.strptime("19 AUG 2018", "%d %b %Y").date()
        table = []
        list_recent_births(table)
        self.assertCountEqual([get_individual("I1").name, get_individual("I2").name, get_individual("I3").name,
                               get_individual("I4").name], table[0][4].split("\n")) and self.assertTrue(table[0][3])

    def test_all_far_births(self):
        get_individual("I1").birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        get_individual("I4").birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        table = []
        list_recent_births(table)
        self.assertFalse(table[0][4].split()) and self.assertTrue(table[0][3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
