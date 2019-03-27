import unittest
from parse_gedcom import *
from io import StringIO
from contextlib import redirect_stdout


class TestUserStory12(unittest.TestCase):
    def setUp(self):
        child = Individual("I1")
        child.name = "Mark /Rivers/"
        child.sex = "M"
        child.birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        child.child_id = "F1"

        dad = Individual("I2")
        dad.name = "Jason /Rivers/"
        dad.sex = "M"
        dad.birth = datetime.strptime("19 SEP 1960", "%d %b %Y").date()
        dad.spouse_id = "F1"

        mom = Individual("I3")
        mom.name = "Abigail /Glute/"
        mom.sex = "F"
        mom.birth = datetime.strptime("3 OCT 1965", "%d %b %Y").date()
        mom.spouse_id = "F1"

        fam1 = Family("F1")
        fam1.husband = "I2"
        fam1.wife = "I3"
        fam1.children.append("I1")
        fam1.marriage = datetime.strptime("29 JUL 1986", "%d %b %Y").date()

        individuals.append(child)
        individuals.append(dad)
        individuals.append(mom)

        families.append(fam1)

    def test_both_parents_too_old(self):
        capture = StringIO()
        get_individual("I2").birth = datetime.strptime("19 SEP 1906", "%d %b %Y").date()
        get_individual("I3").birth = datetime.strptime("3 OCT 1926", "%d %b %Y").date()

        with redirect_stdout(capture):
            parents_not_too_old()

        self.assertIn("Some parents are too old in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_dad_too_old(self):
        capture = StringIO()
        get_individual("I2").birth = datetime.strptime("19 SEP 1906", "%d %b %Y").date()

        with redirect_stdout(capture):
            parents_not_too_old()

        self.assertIn("Some parents are too old in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_mom_too_old(self):
        capture = StringIO()
        get_individual("I3").birth = datetime.strptime("3 OCT 1926", "%d %b %Y").date()

        with redirect_stdout(capture):
            parents_not_too_old()

        self.assertIn("Some parents are too old in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_neither_parents_too_old(self):
        capture = StringIO()
        get_individual("I2").birth = datetime.strptime("19 SEP 1960", "%d %b %Y").date()
        get_individual("I3").birth = datetime.strptime("3 OCT 1965", "%d %b %Y").date()

        with redirect_stdout(capture):
            parents_not_too_old()

        self.assertIn("All parents are not too old in this GEDCOM file.", capture.getvalue().strip().split("\n"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
