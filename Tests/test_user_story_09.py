import unittest
from parse_gedcom import *


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
        get_individual("I2").death = None
        get_individual("I3").death = None
        table = []
        birth_before_parents_death(table)
        self.assertTrue(table[0][3])

    def test_both_parents_dead_pass(self):
        get_individual("I2").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()
        get_individual("I3").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()
        table = []
        birth_before_parents_death(table)
        self.assertTrue(table[0][3])

    def test_both_parents_dead_fail(self):
        get_individual("I2").death = datetime.strptime("3 OCT 1986", "%d %b %Y").date()
        get_individual("I3").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()
        table = []
        birth_before_parents_death(table)
        self.assertFalse(table[0][3])

    def test_dad_dead_pass(self):
        get_individual("I2").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()
        get_individual("I3").death = None
        table = []
        birth_before_parents_death(table)
        self.assertTrue(table[0][3])

    def test_dad_dead_fail(self):
        get_individual("I2").death = datetime.strptime("3 OCT 1986", "%d %b %Y").date()
        get_individual("I3").death = None
        table = []
        birth_before_parents_death(table)
        self.assertFalse(table[0][3])

    def test_mom_dead_pass(self):
        get_individual("I2").death = None
        get_individual("I3").death = datetime.strptime("3 OCT 1988", "%d %b %Y").date()
        table = []
        birth_before_parents_death(table)
        self.assertTrue(table[0][3])

    def test_mom_dead_fail(self):
        get_individual("I2").death = None
        get_individual("I3").death = datetime.strptime("3 OCT 1986", "%d %b %Y").date()
        table = []
        birth_before_parents_death(table)
        self.assertFalse(table[0][3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
