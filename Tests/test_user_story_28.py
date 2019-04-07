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

        individuals.append(child_one)
        individuals.append(child_two)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_no_children(self):
        fam = Family("F1")
        families.append(fam)
        order_children_by_age()
        self.assertFalse(fam.children)

    def test_one_children(self):
        fam = Family("F1")
        fam.children.append("I1")
        families.append(fam)
        order_children_by_age()
        self.assertEqual(["I1"], fam.children)

    def test_twins(self):
        fam = Family("F1")
        fam.children.append("I1")
        fam.children.append("I2")
        families.append(fam)
        order_children_by_age()
        self.assertEqual(["I1", "I2"], fam.children)

    def test_twins_reverse(self):
        fam = Family("F1")
        fam.children.append("I2")
        fam.children.append("I1")
        families.append(fam)
        order_children_by_age()
        self.assertEqual(["I2", "I1"], fam.children)

    def test_not_twins(self):
        fam = Family("F1")
        get_individual("I2").birth = datetime.strptime("25 AUG 1999", "%d %b %Y").date()
        fam.children.append("I1")
        fam.children.append("I2")
        families.append(fam)
        order_children_by_age()
        self.assertEqual(["I1", "I2"], fam.children)

    def test_not_twins_reverse(self):
        fam = Family("F1")
        get_individual("I2").birth = datetime.strptime("25 AUG 1999", "%d %b %Y").date()
        fam.children.append("I2")
        fam.children.append("I1")
        families.append(fam)
        order_children_by_age()
        self.assertEqual(["I1", "I2"], fam.children)


if __name__ == "__main__":
    unittest.main(verbosity=2)
