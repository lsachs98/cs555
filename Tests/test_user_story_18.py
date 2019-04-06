import unittest
from parse_gedcom import *
from io import StringIO
from contextlib import redirect_stdout


class TestUserStory18(unittest.TestCase):
    def setUp(self):
        child1 = Individual("I1")
        child1.name = "Mark /Rivers/"
        child1.sex = "M"
        child1.birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        child1.child_id = "F1"
        child1.spouse_id = "F2"

        child2 = Individual("I2")
        child2.name = "Mary /Rivers/"
        child2.sex = "F"
        child2.birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        child2.child_id = "F1"

        dad = Individual("I3")
        dad.name = "Jason /Rivers/"
        dad.sex = "M"
        dad.birth = datetime.strptime("19 SEP 1960", "%d %b %Y").date()
        dad.spouse_id = "F1"

        mom = Individual("I4")
        mom.name = "Abigail /Rivers/"
        mom.sex = "F"
        mom.birth = datetime.strptime("3 OCT 1965", "%d %b %Y").date()
        mom.spouse_id = "F1"

        fam1 = Family("F1")
        fam1.husband = "I3"
        fam1.wife = "I4"
        fam1.children.append("I1")
        fam1.children.append("I2")
        fam1.marriage = datetime.strptime("29 JUL 1986", "%d %b %Y").date()

        spouse = Individual("I5")
        spouse.name = "Rachel /Rivers/"
        spouse.sex = "F"
        spouse.birth = datetime.strptime("29 FEB 1992", "%d %b %Y").date()
        spouse.spouse_id = "F2"

        fam2 = Family("F2")
        fam2.husband = "I1"
        fam2.wife = "I5"
        fam2.marriage = datetime.strptime("17 AUG 2014", "%d %b %Y").date()

        individuals.append(child1)
        individuals.append(child2)
        individuals.append(dad)
        individuals.append(mom)
        individuals.append(spouse)

        families.append(fam1)
        families.append(fam2)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_siblings_marriage_pass(self):
        capture = StringIO()

        with redirect_stdout(capture):
            siblings_should_not_marry()

        self.assertIn("All siblings are not married.", capture.getvalue().strip().split("\n"))

    def test_siblings_marriage_fail(self):
        capture = StringIO()
        get_individual("I5").spouse_id = None
        get_individual("I2").spouse_id = "F2"
        get_family("F2").wife = "I2"

        with redirect_stdout(capture):
            siblings_should_not_marry()

        self.assertIn("Some siblings are married.", capture.getvalue().strip().split("\n"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
