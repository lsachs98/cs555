import unittest
from US35 import *
from US36 import *
from project03 import *


class Test(unittest.TestCase):

    def test_mix(self):
        personOne = Individual("@I1@")
        personOne.set_name("recentbirthfardeath")
        personOne.set_birth("20 AUG 2018")
        personOne.set_death("20 AUG 2000")
        personTwo = Individual("@I2@")
        personTwo.set_name("farbirthrecentdeath")
        personTwo.set_birth("21 AUG 1998")
        personTwo.set_death("20 AUG 2018")
        personThree = Individual("@I3@")
        personThree.set_name("fardeathandbirth")
        personThree.set_birth("22 AUG 1998")
        personThree.set_death("20 AUG 2000")
        personFour = Individual("@I4@")
        personFour.set_name("recentbirthanddeath")
        personFour.set_birth("12 AUG 2018")
        personFour.set_death("20 AUG 2018")
        self.assertTrue("@I1@" == list_recent_births([personOne,personTwo, personThree, personFour])[0][0])
        self.assertTrue("@I4@" == list_recent_births([personOne,personTwo, personThree, personFour])[1][0])
        self.assertTrue("@I2@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[0][0])
        self.assertTrue("@I4@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[1][0])


    def test_empty_file(self):
        self.assertTrue([] == list_recent_births([]))
        self.assertTrue([] == list_recent_deaths([]))



    def test_all_recent_death_mix_birth(self):
        personOne = Individual("@I1@")
        personOne.set_name("recentbirthfardeath")
        personOne.set_birth("20 AUG 2018")
        personOne.set_death("20 AUG 2018")
        personTwo = Individual("@I2@")
        personTwo.set_name("farbirthrecentdeath")
        personTwo.set_birth("21 AUG 1998")
        personTwo.set_death("20 AUG 2018")
        personThree = Individual("@I3@")
        personThree.set_name("fardeathandbirth")
        personThree.set_birth("22 AUG 1998")
        personThree.set_death("20 AUG 2018")
        personFour = Individual("@I4@")
        personFour.set_name("recentbirthanddeath")
        personFour.set_birth("12 AUG 2018")
        personFour.set_death("20 AUG 2018")
        self.assertTrue("@I1@" == list_recent_births([personOne,personTwo, personThree, personFour])[0][0])
        self.assertTrue("@I4@" == list_recent_births([personOne,personTwo, personThree, personFour])[1][0])
        self.assertTrue("@I1@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[0][0])
        self.assertTrue("@I2@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[1][0])
        self.assertTrue("@I3@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[2][0])
        self.assertTrue("@I4@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[3][0])

    def test_all_recent_birth_mix_death(self):
        personOne = Individual("@I1@")
        personOne.set_name("recentbirthrecentdeath1")
        personOne.set_birth("20 AUG 2018")
        personOne.set_death("20 AUG 2018")
        personTwo = Individual("@I2@")
        personTwo.set_name("recentbirthrecentdeath2")
        personTwo.set_birth("21 AUG 2018")
        personTwo.set_death("23 AUG 2018")
        personThree = Individual("@I3@")
        personThree.set_name("recentbirthfardeath1")
        personThree.set_birth("22 AUG 2018")
        personThree.set_death("20 AUG 2017")
        personFour = Individual("@I4@")
        personFour.set_name("recentbirthfardeath2")
        personFour.set_birth("02 AUG 2018")
        personFour.set_death("20 AUG 2017")
        print(list_recent_births([personOne,personTwo, personThree, personFour]))
        self.assertTrue("@I1@" == list_recent_births([personOne,personTwo, personThree, personFour])[0][0])
        self.assertTrue("@I2@" == list_recent_births([personOne,personTwo, personThree, personFour])[1][0])
        self.assertTrue("@I3@" == list_recent_births([personOne,personTwo, personThree, personFour])[2][0])
        self.assertTrue("@I4@" == list_recent_births([personOne,personTwo, personThree, personFour])[3][0])
        self.assertTrue("@I1@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[0][0])
        self.assertTrue("@I2@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[1][0])
        

    def test_all_recent_death_all_recent_birth(self):
        personOne = Individual("@I1@")
        personOne.set_name("recentbirthanddeath1")
        personOne.set_birth("20 AUG 2018")
        personOne.set_death("20 AUG 2018")
        personTwo = Individual("@I2@")
        personTwo.set_name("recentbirthanddeath2")
        personTwo.set_birth("21 AUG 2018")
        personTwo.set_death("20 AUG 2018")
        personThree = Individual("@I3@")
        personThree.set_name("recentbirthanddeath3")
        personThree.set_birth("22 AUG 2018")
        personThree.set_death("20 AUG 2018")
        personFour = Individual("@I4@")
        personFour.set_name("recentbirthanddeath4")
        personFour.set_birth("02 AUG 2018")
        personFour.set_death("20 AUG 2018")
        self.assertTrue("@I1@" == list_recent_births([personOne,personTwo, personThree, personFour])[0][0])
        self.assertTrue("@I2@" == list_recent_births([personOne,personTwo, personThree, personFour])[1][0])
        self.assertTrue("@I3@" == list_recent_births([personOne,personTwo, personThree, personFour])[2][0])
        self.assertTrue("@I4@" == list_recent_births([personOne,personTwo, personThree, personFour])[3][0])
        self.assertTrue("@I1@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[0][0])
        self.assertTrue("@I2@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[1][0])
        self.assertTrue("@I3@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[2][0])
        self.assertTrue("@I4@" == list_recent_deaths([personOne,personTwo, personThree, personFour])[3][0])

    def test_all_far_death_all_far_birth(self):
        personOne = Individual("@I1@")
        personOne.set_name("farbirthanddeath1")
        personOne.set_birth("20 AUG 2017")
        personOne.set_death("20 AUG 2017")
        personTwo = Individual("@I2@")
        personTwo.set_name("rfarbirthanddeath2")
        personTwo.set_birth("21 AUG 2017")
        personTwo.set_death("20 AUG 2017")
        personThree = Individual("@I3@")
        personThree.set_name("farbirthanddeath3")
        personThree.set_birth("22 AUG 2017")
        personThree.set_death("20 AUG 2017")
        personFour = Individual("@I4@")
        personFour.set_name("farbirthanddeath4")
        personFour.set_birth("02 AUG 2017")
        personFour.set_death("20 AUG 2017")
        self.assertTrue([] == list_recent_births([]))
        self.assertTrue([] == list_recent_deaths([]))

    
   
if __name__ == '__main__':
        unittest.main()
        
