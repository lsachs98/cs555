import unittest
from parse_gedcom import *


class TestUserStory28(unittest.TestCase):
    def setUp(self):
        child_one = Individual("I1")
        child_one.name = "Lauren /Sachs/"
        child_one.birth = datetime.strptime("25 AUG 1998", "%d %b %Y").date()
        child_two = Individual("I2")
        child_two.name = "Lauren /Sachs/"
        child_two.birth = datetime.strptime("25 AUG 1998", "%d %b %Y").date()
        dad = Individual("I3")
        dad.name = "Larry /Sachs/"
        dad.birth = datetime.strptime("25 AUG 1968", "%d %b %Y").date()
        mom = Individual("I4")
        mom.name = "Lauren /Sachs/"
        mom.birth = datetime.strptime("25 AUG 1967", "%d %b %Y").date()

        individuals.append(child_one)
        individuals.append(child_two)
        individuals.append(dad)
        individuals.append(mom)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_no_children(self):
        table = []
        fam = Family("F1")
        fam.husband = "I3"
        fam.wife = "I4"
        families.append(fam)
        order_children_by_age(table)
        self.assertFalse(fam.children) and self.assertTrue(table[0][3])

    def test_one_children(self):
        table = []
        fam = Family("F1")
        fam.children.append("I1")
        fam.husband = "I3"
        fam.wife = "I4"
        families.append(fam)
        order_children_by_age(table)
        self.assertEqual(["I1"], fam.children) and self.assertTrue(table[0][3])

    def test_twins(self):
        table = []
        fam = Family("F1")
        fam.children.append("I1")
        fam.children.append("I2")
        fam.husband = "I3"
        fam.wife = "I4"
        families.append(fam)
        order_children_by_age(table)
        self.assertEqual(["I1", "I2"], fam.children) and self.assertTrue(table[0][3])

    def test_twins_reverse(self):
        table = []
        fam = Family("F1")
        fam.children.append("I2")
        fam.children.append("I1")
        fam.husband = "I3"
        fam.wife = "I4"
        families.append(fam)
        order_children_by_age(table)
        self.assertEqual(["I2", "I1"], fam.children) and self.assertTrue(table[0][3])

    def test_not_twins(self):
        table = []
        fam = Family("F1")
        get_individual("I2").birth = datetime.strptime("25 AUG 1999", "%d %b %Y").date()
        fam.children.append("I1")
        fam.children.append("I2")
        fam.husband = "I3"
        fam.wife = "I4"
        families.append(fam)
        order_children_by_age(table)
        self.assertEqual(["I1", "I2"], fam.children) and self.assertTrue(table[0][3])

    def test_not_twins_reverse(self):
        table = []
        fam = Family("F1")
        get_individual("I2").birth = datetime.strptime("25 AUG 1999", "%d %b %Y").date()
        fam.children.append("I2")
        fam.children.append("I1")
        fam.husband = "I3"
        fam.wife = "I4"
        families.append(fam)
        order_children_by_age(table)
        self.assertEqual(["I1", "I2"], fam.children) and self.assertTrue(table[0][3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
