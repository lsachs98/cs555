import unittest
from parse_gedcom import *
from io import StringIO
from contextlib import redirect_stdout


class TestUserStory16(unittest.TestCase):
    def setUp(self):
        dad = Individual("I1")
        dad.name = "Mark /Rivers/"
        dad.sex = "M"
        dad.spouse_id = "F1"
        son1 = Individual("I2")
        son1.name = "John /Rivers/"
        son1.sex = "M"
        son1.child_id = "F1"
        son2 = Individual("I3")
        son2.name = "David /Rivers/"
        son2.sex = "M"
        son2.child_id = "F1"
        fam = Family("F1")
        fam.husband = "I1"
        fam.children.append("I2")
        fam.children.append("I3")
        individuals.append(dad)
        individuals.append(son1)
        individuals.append(son2)
        families.append(fam)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_no_children(self):
        capture = StringIO()
        families.clear()

        with redirect_stdout(capture):
            male_last_names()

        self.assertIn("All male children have their father's last name.", capture.getvalue().strip().split("\n"))

    def test_daughters(self):
        capture = StringIO()

        get_individual("I2").sex = "F"
        get_individual("I3").sex = "F"

        with redirect_stdout(capture):
            male_last_names()

        self.assertIn("All male children have their father's last name.", capture.getvalue().strip().split("\n"))

    def test_sons_match_father(self):
        capture = StringIO()

        with redirect_stdout(capture):
            male_last_names()

        self.assertIn("All male children have their father's last name.", capture.getvalue().strip().split("\n"))

    def test_one_son_matches_father(self):
        capture = StringIO()

        get_individual("I3").name = "David /Doe/"

        with redirect_stdout(capture):
            male_last_names()

        self.assertIn("Some male children don't have their father's last name.", capture.getvalue().strip().split("\n"))

    def test_no_son_matches_father(self):
        capture = StringIO()

        get_individual("I2").name = "John /Smith/"
        get_individual("I3").name = "David /Doe/"

        with redirect_stdout(capture):
            male_last_names()

        self.assertIn("Some male children don't have their father's last name.", capture.getvalue().strip().split("\n"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
