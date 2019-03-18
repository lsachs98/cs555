from unittest import TestCase
from parse_gedcom import *


class TestUserStory09(TestCase):
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
        family = Family("F1")
        family.husband = "I2"
        family.wife = "I3"
        family.children.append("I1")
        family.marriage = datetime.strptime("29 JUL 1986", "%d %b %Y").date()
        families.append(family)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_get_husband_id(self):
        self.assertEqual(get_husband_id(individuals[0]), "I2")

    def test_get_wife_id(self):
        self.assertEqual(get_wife_id(individuals[0]), "I3")

    def test_get_husband(self):
        self.assertEqual(get_husband("I2"), individuals[1])

    def test_get_wife(self):
        self.assertEqual(get_wife("I3"), individuals[2])

    def test_user_story_09(self):
        self.assertTrue(user_story_09(individuals[0]), individuals[0])
