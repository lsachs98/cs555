import unittest
from parse_gedcom import *


class TestUserStory30(unittest.TestCase):
    def setUp(self):
        ind1 = Individual("I1")
        ind1.name = "Single /Living1/"
        ind1.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        ind2 = Individual("I2")
        ind2.name = "Single /Living2/"
        ind2.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        ind3 = Individual("I3")
        ind3.name = "Single /Living3/"
        ind3.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()
        ind4 = Individual("I4")
        ind4.name = "Single /Living4/"
        ind4.birth = datetime.strptime("20 AUG 1998", "%d %b %Y").date()

        individuals.append(ind1)
        individuals.append(ind2)
        individuals.append(ind3)
        individuals.append(ind4)

    def tearDown(self):
        individuals.clear()

    def test_empty_file(self):
        individuals.clear()
        table = []
        list_living_married(table)
        self.assertFalse(table[0][4].split()) and self.assertTrue(table[0][3])

    def test_some_married_and_some_deceased(self):
        get_individual("I2").name = "Married /Living2/"
        get_individual("I2").spouse_id = "F1"
        get_individual("I3").name = "Married /Deceased3/"
        get_individual("I3").spouse_id = "F1"
        get_individual("I3").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I4").name = "Single /Deceased4/"
        get_individual("I4").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        table = []
        list_living_married(table)
        self.assertCountEqual([get_individual("I2").name], table[0][4].split("\n")) and self.assertTrue(table[0][3])

    def test_some_married_and_all_deceased(self):
        get_individual("I1").name = "Single /Deceased1/"
        get_individual("I1").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I2").name = "Married /Deceased2/"
        get_individual("I2").spouse_id = "F1"
        get_individual("I2").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I3").name = "Married /Deceased3/"
        get_individual("I3").spouse_id = "F1"
        get_individual("I3").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I4").name = "Single /Deceased4/"
        get_individual("I4").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        table = []
        list_living_married(table)
        self.assertFalse(table[0][4].split()) and self.assertTrue(table[0][3])

    def test_some_married_and_no_deceased(self):
        get_individual("I2").name = "Married /Living2/"
        get_individual("I2").spouse_id = "F1"
        get_individual("I3").name = "Married /Living3/"
        get_individual("I3").spouse_id = "F1"
        table = []
        list_living_married(table)
        self.assertCountEqual([get_individual("I2").name, get_individual("I3").name], table[0][4].split("\n")) and self.assertTrue(table[0][3])

    def test_all_married_and_some_deceased(self):
        families.append(Family("F2"))
        get_individual("I1").name = "Married /Deceased1/"
        get_individual("I1").spouse_id = "F2"
        get_individual("I1").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I4").name = "Married /Deceased4/"
        get_individual("I4").spouse_id = "F2"
        get_individual("I4").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I2").spouse_id = "F1"
        get_individual("I3").spouse_id = "F1"
        table = []
        list_living_married(table)
        self.assertCountEqual([get_individual("I2").name, get_individual("I3").name], table[0][4].split("\n")) and self.assertTrue(table[0][3])

    def test_no_married_and_some_deceased(self):
        get_individual("I2").name = "Single /Deceased2/"
        get_individual("I2").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        get_individual("I3").name = "Single /Deceased3/"
        get_individual("I3").death = datetime.strptime("20 AUG 2000", "%d %b %Y").date()
        table = []
        list_living_married(table)
        self.assertFalse(table[0][4].split()) and self.assertTrue(table[0][3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
