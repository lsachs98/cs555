import unittest
from US_29 import *
from parse_to_objects import *


class Test(unittest.TestCase):

    def test_no_deceased(self):
        myGED = GEDInfo()
        personOne = Individual("@I1@")
        personOne.set_name("notdeceased1")
        personOne.set_birth("20 AUG 1998")
        personTwo = Individual("@I2@")
        personTwo.set_name("notdeceased2")
        personTwo.set_birth("21 AUG 1998")
        personThree = Individual("@I3@")
        personThree.set_name("notdeceased3")
        personThree.set_birth("22 AUG 1998")
        personFour = Individual("@I4@")
        personFour.set_name("notdeceased4")
        personFour.set_birth("25 AUG 1998")
        myGED.set_families([])
        myGED.set_individuals([personOne,personTwo, personThree, personFour])
        self.assertTrue([] == list_deceased(myGED))



    def test_all_deceased(self):
        myGED = GEDInfo()
        personOne = Individual("@I1@")
        personOne.set_name("deceased1")
        personOne.set_birth("20 AUG 1998")
        personOne.set_death("20 AUG 2000")
        personTwo = Individual("@I2@")
        personTwo.set_name("deceased2")
        personTwo.set_birth("21 AUG 1998")
        personTwo.set_death("20 AUG 2000")
        personThree = Individual("@I3@")
        personThree.set_name("deceased3")
        personThree.set_birth("22 AUG 1998")
        personThree.set_death("20 AUG 2000")
        personFour = Individual("@I4@")
        personFour.set_name("deceased4")
        personFour.set_birth("25 AUG 1998")
        personFour.set_death("20 AUG 2000")
        myGED.set_families([])
        myGED.set_individuals([personOne,personTwo, personThree, personFour])
        self.assertTrue(["@I1@","@I2@","@I3@","@I4@"] == list_deceased(myGED))


    def test_empty_file(self):
        myGED = GEDInfo()
        myGED.set_individuals([])
        myGED.set_families([])
        self.assertEqual([], list_deceased(myGED))

    def test_one_deceased(self):
        myGED = GEDInfo()
        personOne = Individual("@I1@")
        personOne.set_name("deceased1")
        personOne.set_birth("20 AUG 1998")
        personOne.set_death("20 AUG 2000")
        personTwo = Individual("@I2@")
        personTwo.set_name("notdeceased2")
        personTwo.set_birth("21 AUG 1998")
        personThree = Individual("@I3@")
        personThree.set_name("notdeceased3")
        personThree.set_birth("22 AUG 1998")
        personFour = Individual("@I4@")
        personFour.set_name("notdeceased4")
        personFour.set_birth("25 AUG 1998")
        myGED.set_families([])
        myGED.set_individuals([personOne,personTwo, personThree, personFour])
        self.assertEqual(["@I1@"],list_deceased(myGED))



    def test_many_deceased(self):
        myGED = GEDInfo()
        personOne = Individual("@I1@")
        personOne.set_name("deceased1")
        personOne.set_birth("20 AUG 1998")
        personOne.set_death("20 AUG 2000")
        personTwo = Individual("@I2@")
        personTwo.set_name("deceased2")
        personTwo.set_birth("21 AUG 1998")
        personTwo.set_death("20 AUG 2000")
        personThree = Individual("@I3@")
        personThree.set_name("deceased3")
        personThree.set_birth("22 AUG 1998")
        personThree.set_death("20 AUG 2000")
        personFour = Individual("@I4@")
        personFour.set_name("notdeceased4")
        personFour.set_birth("25 AUG 1998")
        myGED.set_families([])
        myGED.set_individuals([personOne,personTwo, personThree, personFour])
        self.assertEqual(["@I1@","@I2@","@I3@"],list_deceased(myGED))


   
if __name__ == '__main__':
        unittest.main()
        
