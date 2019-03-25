import unittest
from US29_refactored import *
from parse_to_objects_refactored import *


class Test(unittest.TestCase):

    def test_no_deceased(self):
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
        self.assertTrue([] == list_deceased([personOne,personTwo, personThree, personFour]))



    def test_all_deceased(self):
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
        self.assertTrue(["@I1@","@I2@","@I3@","@I4@"] == list_deceased([personOne,personTwo, personThree, personFour]))


    def test_empty_file(self):
        self.assertEqual([], list_deceased([]))

    def test_one_deceased(self):
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
        self.assertEqual(["@I1@"],list_deceased([personOne,personTwo, personThree, personFour]))



    def test_many_deceased(self):
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
        self.assertEqual(["@I1@","@I2@","@I3@"],list_deceased([personOne,personTwo, personThree, personFour]))


   
if __name__ == '__main__':
        unittest.main()
        
