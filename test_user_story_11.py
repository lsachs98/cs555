import unittest
from parse_gedcom import *
from io import StringIO
from contextlib import redirect_stdout


class TestUserStory11(unittest.TestCase):
    def setUp(self):
        child = Individual("I1")
        child.name = "Mark /Rivers/"
        child.sex = "M"
        child.birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        child.child_id = "F1"

        hus = Individual("I2")
        hus.name = "Jason /Rivers/"
        hus.sex = "M"
        hus.birth = datetime.strptime("19 SEP 1960", "%d %b %Y").date()
        hus.spouse_id = "F1"

        wife1 = Individual("I3")
        wife1.name = "Abigail /Glute/"
        wife1.sex = "F"
        wife1.birth = datetime.strptime("3 OCT 1965", "%d %b %Y").date()
        wife1.spouse_id = "F1"

        wife2 = Individual("I4")
        wife2.name = "Brittany /Spears/"
        wife2.sex = "F"
        wife2.birth = datetime.strptime("13 JUN 1985", "%d %b %Y").date()
        wife2.spouse_id = "F2"

        fam1 = Family("F1")
        fam1.husband = "I2"
        fam1.wife = "I3"
        fam1.children.append("I1")
        fam1.marriage = datetime.strptime("29 JUL 1986", "%d %b %Y").date()

        fam2 = Family("F2")
        fam2.husband = "I2"
        fam2.wife = "I4"
        fam2.children.append("I1")
        fam2.marriage = datetime.strptime("17 DEC 2006", "%d %b %Y").date()

        individuals.append(child)
        individuals.append(hus)
        individuals.append(wife1)
        individuals.append(wife2)

        families.append(fam1)
        families.append(fam2)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_less_than_two_marriages(self):
        capture = StringIO()
        individuals.pop()
        individuals.pop()
        families.clear()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are no bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_no_divorce_spouse_death_pass(self):
        capture = StringIO()
        get_individual("I3").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are no bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_no_divorce_spouse_death_fail(self):
        capture = StringIO()
        get_individual("I3").death = datetime.strptime("3 OCT 2007", "%d %b %Y").date()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_one_divorce_pass(self):
        capture = StringIO()
        get_family("F1").divorce = datetime.strptime("3 OCT 1990", "%d %b %Y").date()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are no bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_one_divorce_fail(self):
        capture = StringIO()
        get_family("F1").divorce = datetime.strptime("3 OCT 2007", "%d %b %Y").date()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_one_divorce_spouse_death_pass(self):
        capture = StringIO()
        get_family("F1").divorce = datetime.strptime("3 OCT 1987", "%d %b %Y").date()
        get_individual("I3").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are no bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_one_divorce_spouse_death_fail(self):
        capture = StringIO()
        get_family("F1").divorce = datetime.strptime("3 OCT 2007", "%d %b %Y").date()
        get_individual("I3").death = datetime.strptime("3 OCT 2009", "%d %b %Y").date()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_both_divorce_spouse_death_pass(self):
        capture = StringIO()
        get_family("F1").divorce = datetime.strptime("3 OCT 1997", "%d %b %Y").date()
        get_family("F2").divorce = datetime.strptime("3 OCT 2014", "%d %b %Y").date()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are no bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))

    def test_both_divorce_spouse_death_fail(self):
        capture = StringIO()
        get_family("F1").divorce = datetime.strptime("3 OCT 2007", "%d %b %Y").date()
        get_family("F2").divorce = datetime.strptime("3 OCT 2014", "%d %b %Y").date()

        with redirect_stdout(capture):
            no_bigamy()

        self.assertIn("There are bigamy cases in this GEDCOM file.", capture.getvalue().strip().split("\n"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
