import unittest
from parse_gedcom import *


class TestUserStory17(unittest.TestCase):
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

        child3 = Individual("I6")
        child3.name = "Timothy /Rivers/"
        child3.sex = "M"
        child3.birth = datetime.strptime("13 DEC 2011", "%d %b %Y").date()
        child3.child_id = "F2"

        fam2 = Family("F2")
        fam2.husband = "I1"
        fam2.wife = "I5"
        fam2.marriage = datetime.strptime("17 AUG 2014", "%d %b %Y").date()
        fam2.children.append("I6")

        individuals.append(child1)
        individuals.append(child2)
        individuals.append(dad)
        individuals.append(mom)
        individuals.append(spouse)
        individuals.append(child3)

        families.append(fam1)
        families.append(fam2)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_no_ancestor_descendant_marriages(self):
        table = []
        no_marriage_to_descendants(table)
        self.assertTrue(table[0][3])

    def test_immediate_ancestor_descendant_marriage(self):
        table = []
        get_family("F1").divorce = datetime.strptime("21 MAY 1998", "%d %b %Y").date()
        get_individual("I3").spouse_id = "F3"
        get_individual("I2").spouse_id = "F3"
        get_individual("I4").spouse_id = None
        incest = Family("F3")
        incest.husband = "I3"
        incest.wife = "I2"
        incest.marriage = datetime.strptime("3 MAR 2000", "%d %b %Y").date()
        families.append(incest)
        no_marriage_to_descendants(table)
        self.assertFalse(table[0][3])

    def test_grandchild_ancestor_descendant_marriages(self):
        table = []
        get_family("F1").divorce = datetime.strptime("21 MAY 1998", "%d %b %Y").date()
        get_individual("I4").spouse_id = "F3"
        get_individual("I6").spouse_id = "F3"
        get_individual("I3").spouse_id = None
        incest = Family("F3")
        incest.husband = "I6"
        incest.wife = "I4"
        incest.marriage = datetime.strptime("3 MAR 2000", "%d %b %Y").date()
        families.append(incest)
        no_marriage_to_descendants(table)
        self.assertFalse(table[0][3])


if __name__ == '__main__':
    unittest.main(verbosity=2)
