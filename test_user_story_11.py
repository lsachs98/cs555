from unittest import TestCase
from parse_gedcom import *


class TestUserStory11(TestCase):
    def setUp(self):
        print(self._testMethodName)
        child = Individual("I1")
        child.name = "Mark /Rivers/"
        child.sex = "M"
        child.birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        child.child_id = "F1"
        individuals.append(child)
        hus = Individual("I2")
        hus.name = "Jason /Rivers/"
        hus.sex = "M"
        hus.birth = datetime.strptime("19 SEP 1960", "%d %b %Y").date()
        hus.spouse_id = "F1"
        individuals.append(hus)
        wife = Individual("I3")
        wife.name = "Abigail /Glute/"
        wife.sex = "F"
        wife.birth = datetime.strptime("3 OCT 1965", "%d %b %Y").date()
        wife.spouse_id = "F1"
        individuals.append(wife)
        wife = Individual("I4")
        wife.name = "Brittany /Spears/"
        wife.sex = "F"
        wife.birth = datetime.strptime("13 JUN 1985", "%d %b %Y").date()
        wife.spouse_id = "F2"
        individuals.append(wife)
        hus = Individual("I5")
        hus.name = "Bruce /Wayne/"
        hus.sex = "M"
        hus.birth = datetime.strptime("27 FEB 1970", "%d %b %Y").date()
        hus.spouse_id = "F3"
        individuals.append(hus)
        family = Family("F1")
        family.husband = "I2"
        family.wife = "I3"
        family.children.append("I1")
        family.marriage = datetime.strptime("29 JUL 1986", "%d %b %Y").date()
        families.append(family)
        family = Family("F2")
        family.husband = "I2"
        family.wife = "I4"
        family.children.append("I1")
        family.marriage = datetime.strptime("17 DEC 2006", "%d %b %Y").date()
        families.append(family)
        family = Family("F3")
        family.husband = "I5"
        family.wife = "I3"
        family.children.append("I1")
        family.marriage = datetime.strptime("17 DEC 1980", "%d %b %Y").date()
        family.divorce = datetime.strptime("7 NOV 1983", "%d %b %Y").date()
        families.append(family)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_user_story_11(self):
        self.assertFalse(user_story_11(individuals[0]), individuals[0])  # no marriage
        self.assertTrue(user_story_11(individuals[1]), individuals[1])  # bigotry
        self.assertFalse(user_story_11(individuals[2]), individuals[2])  # one divorce, no bigotry
        # TODO finish tests
