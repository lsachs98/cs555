import unittest
from parse_gedcom import *


class TestUserStory30(unittest.TestCase):
    def setUp(self):
        ind1 = Individual("I1")
        ind1.name = "Not /Deceased1/"
        ind1.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        ind2 = Individual("I2")
        ind1.name = "Not /Deceased2/"
        ind1.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        ind3 = Individual("I3")
        ind1.name = "Not /Deceased3/"
        ind1.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        ind4 = Individual("I4")
        ind1.name = "Not /Deceased4/"
        ind1.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()

        individuals.append(ind1)
        individuals.append(ind2)
        individuals.append(ind3)
        individuals.append(ind4)

    def tearDown(self):
        individuals.clear()

    def test_empty_file(self):
        individuals.clear()
        self.assertFalse(list_deceased())

    def test_no_deceased(self):
        self.assertFalse(list_deceased())

    def test_one_deceased(self):
        get_individual("I1").name = "Is /Deceased1/"
        get_individual("I1").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        self.assertCountEqual([get_individual("I1")], list_deceased())

    def test_many_deceased(self):
        get_individual("I1").name = "Is /Deceased1/"
        get_individual("I1").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I2").name = "Is /Deceased2/"
        get_individual("I2").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I3").name = "Is /Deceased3/"
        get_individual("I3").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        self.assertCountEqual([get_individual("I1"), get_individual("I2"), get_individual("I3")], list_deceased())

    def test_all_deceased(self):
        get_individual("I1").name = "Is /Deceased1/"
        get_individual("I1").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I2").name = "Is /Deceased2/"
        get_individual("I2").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I3").name = "Is /Deceased3/"
        get_individual("I3").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I4").name = "Is /Deceased4/"
        get_individual("I4").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        self.assertCountEqual([get_individual("I1"), get_individual("I2"), get_individual("I3"), get_individual("I4")], list_deceased())


if __name__ == "__main__":
    unittest.main(verbosity=2)
