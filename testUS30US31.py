import unittest
from US30 import *
from US31 import *
from project03 import *


class Test(unittest.TestCase):

    def test_mix(self):
        personOne = Individual("@I1@")
        personOne.set_name("singleandliving")
        personOne.set_birth("20 AUG 1998")
        fam = Family("F1")
        personTwo = Individual("@I2@")
        personTwo.set_name("marriedandliving")
        personTwo.set_spouse("F1")
        personTwo.set_birth("21 AUG 1998")
        personThree = Individual("@I3@")
        personThree.set_name("marriedanddeceased")
        personThree.set_spouse("F1")
        personThree.set_birth("22 AUG 1998")
        personThree.set_death("20 AUG 2000")
        personFour = Individual("@I4@")
        personFour.set_name("singleanddeceased")
        personFour.set_birth("25 AUG 1998")
        personFour.set_death("20 AUG 2000")
        self.assertTrue(["@I2@"] == list_living_married([personOne,personTwo, personThree, personFour]))
        self.assertTrue(["@I1@"] == list_living_single([personOne,personTwo, personThree, personFour]))


    def test_empty_file(self):
        self.assertTrue([] == list_living_married([]))
        self.assertTrue([] == list_living_single([]))



    def test_all_deceased_mix_married(self):
        fam = Family("F1")
        personOne = Individual("@I1@")
        personOne.set_name("deceasedandmarried1")
        personOne.set_birth("20 AUG 1998")
        personOne.set_death("20 AUG 2000")
        personOne.set_spouse("F1")
        personTwo = Individual("@I2@")
        personTwo.set_name("deceasedandmarried2")
        personTwo.set_birth("21 AUG 1998")
        personTwo.set_death("20 AUG 2000")
        personTwo.set_spouse("F1")
        personThree = Individual("@I3@")
        personThree.set_name("deceasedandsingle3")
        personThree.set_birth("22 AUG 1998")
        personThree.set_death("20 AUG 2000")
        personFour = Individual("@I4@")
        personFour.set_name("deceasedandsingle4")
        personFour.set_birth("25 AUG 1998")
        personFour.set_death("20 AUG 2000")
        self.assertTrue([] == list_living_married([personOne,personTwo, personThree, personFour]))
        self.assertTrue([] == list_living_single([personOne,personTwo, personThree, personFour]))

    def test_all_living_mix_married(self):
        fam = Family("F1")
        personOne = Individual("@I1@")
        personOne.set_name("livingmarried1")
        personOne.set_birth("20 AUG 1998")
        personOne.set_spouse("F1")
        personTwo = Individual("@I2@")
        personTwo.set_name("livingmarried2")
        personTwo.set_birth("21 AUG 1998")
        personTwo.set_spouse("F1")
        personThree = Individual("@I3@")
        personThree.set_name("livingsingle3")
        personThree.set_birth("22 AUG 1998")
        personFour = Individual("@I4@")
        personFour.set_name("livingsingle")
        personFour.set_birth("25 AUG 1998")
        self.assertTrue(["@I1@","@I2@"] == list_living_married([personOne,personTwo, personThree, personFour]))
        self.assertTrue(["@I3@","@I4@"] == list_living_single([personOne,personTwo, personThree, personFour]))

    def test_mix_deceased_all_married(self):
        fam1 = Family("F1")
        personOne = Individual("@I1@")
        personOne.set_name("deceasedandmarried1")
        personOne.set_birth("20 AUG 1998")
        personOne.set_spouse("F1")
        personTwo = Individual("@I2@")
        personTwo.set_name("deceasedandmarried2")
        personTwo.set_birth("21 AUG 1998")
        personTwo.set_spouse("F1")
        fam2 = Family("F2")
        personThree = Individual("@I3@")
        personThree.set_name("livingandmarried1")
        personThree.set_birth("22 AUG 1998")
        personThree.set_death("20 AUG 2000")
        personThree.set_spouse("F2")
        personFour = Individual("@I4@")
        personFour.set_name("livingandmarried2")
        personFour.set_birth("25 AUG 1998")
        personFour.set_death("20 AUG 2000")
        personThree.set_spouse("F2")
        self.assertTrue(["@I1@","@I2@"] == list_living_married([personOne,personTwo, personThree, personFour]))
        self.assertTrue([] == list_living_single([personOne,personTwo, personThree, personFour]))

    def test_mix_deceased_all_single(self):
        personOne = Individual("@I1@")
        personOne.set_name("livingandsingle1")
        personOne.set_birth("20 AUG 1998")
        personTwo = Individual("@I2@")
        personTwo.set_name("livingandsingle2")
        personTwo.set_birth("21 AUG 1998")
        personThree = Individual("@I3@")
        personThree.set_name("deceasedandsingle3")
        personThree.set_birth("22 AUG 1998")
        personThree.set_death("20 AUG 2000")
        personFour = Individual("@I4@")
        personFour.set_name("deceasedandsingle4")
        personFour.set_birth("25 AUG 1998")
        personFour.set_death("20 AUG 2000")
        self.assertTrue([] == list_living_married([personOne,personTwo, personThree, personFour]))
        self.assertTrue(["@I1@","@I2@"] == list_living_single([personOne,personTwo, personThree, personFour]))

    
   
if __name__ == '__main__':
        unittest.main()
        
