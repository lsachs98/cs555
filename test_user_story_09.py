import unittest
from parse_gedcom import *
from io import StringIO
from contextlib import redirect_stdout


class TestUserStory09(unittest.TestCase):
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

        family = Family("F1")
        family.husband = "I2"
        family.wife = "I3"
        family.children.append("I1")
        family.marriage = datetime.strptime("29 JUL 1986", "%d %b %Y").date()

        individuals.append(child)
        individuals.append(dad)
        individuals.append(mom)
        families.append(family)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_both_parents_alive(self):
        capture = StringIO()
        get_individual("I2").death = None
        get_individual("I3").death = None

        with redirect_stdout(capture):
            birth_before_parents_death()

        self.assertIn("All birth dates were before parents' deaths.", capture.getvalue().strip().split("\n"))

    def test_both_parents_dead_pass(self):
        capture = StringIO()
        get_individual("I2").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()
        get_individual("I3").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()

        with redirect_stdout(capture):
            birth_before_parents_death()

        self.assertIn("All birth dates were before parents' deaths.", capture.getvalue().strip().split("\n"))

    def test_both_parents_dead_fail(self):
        capture = StringIO()
        get_individual("I2").death = datetime.strptime("3 OCT 1986", "%d %b %Y").date()
        get_individual("I3").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()

        with redirect_stdout(capture):
            birth_before_parents_death()

        self.assertIn("One or more birth dates were incorrect.", capture.getvalue().strip().split("\n"))

    def test_dad_dead_pass(self):
        capture = StringIO()
        get_individual("I2").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()
        get_individual("I3").death = None
        with redirect_stdout(capture):
            birth_before_parents_death()

        self.assertIn("All birth dates were before parents' deaths.", capture.getvalue().strip().split("\n"))

    def test_dad_dead_fail(self):
        capture = StringIO()
        get_individual("I2").death = datetime.strptime("3 OCT 1986", "%d %b %Y").date()
        get_individual("I3").death = None
        with redirect_stdout(capture):
            birth_before_parents_death()

        self.assertIn("One or more birth dates were incorrect.", capture.getvalue().strip().split("\n"))

    def test_mom_dead_pass(self):
        capture = StringIO()
        get_individual("I2").death = None
        get_individual("I3").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()

        with redirect_stdout(capture):
            birth_before_parents_death()

        self.assertIn("All birth dates were before parents' deaths.", capture.getvalue().strip().split("\n"))

    def test_mom_dead_fail(self):
        capture = StringIO()
        get_individual("I2").death = None
        get_individual("I3").death = datetime.strptime("3 OCT 1986", "%d %b %Y").date()
        with redirect_stdout(capture):
            birth_before_parents_death()

        self.assertIn("One or more birth dates were incorrect.", capture.getvalue().strip().split("\n"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
