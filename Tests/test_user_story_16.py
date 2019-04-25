import unittest
from parse_gedcom import *


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
        table = []
        families.clear()
        male_last_names(table)
        self.assertTrue(table[0][3])

    def test_daughters(self):
        table = []
        get_individual("I2").sex = "F"
        get_individual("I3").sex = "F"
        male_last_names(table)
        self.assertTrue(table[0][3])

    def test_sons_match_father(self):
        table = []
        male_last_names(table)
        self.assertTrue(table[0][3])

    def test_one_son_matches_father(self):
        table = []
        get_individual("I3").name = "David /Doe/"
        male_last_names(table)
        self.assertFalse(table[0][3])

    def test_no_son_matches_father(self):
        table = []
        get_individual("I2").name = "John /Smith/"
        get_individual("I3").name = "David /Doe/"
        male_last_names(table)
        self.assertFalse(table[0][3])


if __name__ == '__main__':
    unittest.main(verbosity=2)
