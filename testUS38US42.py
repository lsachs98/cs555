import unittest
from US38 import *
from US42 import *
from parse_gedcom import *
from datetime import datetime, timedelta


class Test(unittest.TestCase):

    def test_valid_upcoming_birthday(self):
        personOne = Individual("@I1@")
        personOne.birth = datetime.today() + timedelta(days = 1)
        self.assertTrue( "@I1@" == list_upcoming_birthdays([personOne])[0][0])
        self.assertTrue(True == reject_invalid_dates(personOne))
                        

    def test_valid_passed_birthday(self):
        personOne = Individual("@I1@")
        personOne.birth = datetime.today() - timedelta(days = 1)
        self.assertTrue( [] == list_upcoming_birthdays([personOne]))
        self.assertTrue(True == reject_invalid_dates(personOne))  

    def test_invalid_upcoming_birthday(self):
        personOne = Individual("@I1@")
        personOne.birth = datetime(datetime.today().year,datetime.today().month,30)
        self.assertTrue( "@I1@" == list_upcoming_birthdays([personOne])[0][0])
        self.assertTrue(False == reject_invalid_dates(personOne))


    def test_invalid_passed_birthday(self):
        personOne = Individual("@I1@")
        personOne.birth = datetime(datetime.today().year,(datetime.today().month + 11) % 12,30)
        self.assertTrue( [] == list_upcoming_birthdays([personOne]))
        self.assertTrue(True == reject_invalid_dates(personOne))
                        

    def test_empty_file(self):
        self.assertTrue([] == list_upcoming_birthdays([]))

    def test_no_dates(self):
        personOne = Individual("@I1@")
        self.assertTrue(True == reject_invalid_dates(personOne))

    def test_leap_year_and_mix_validity(self):
        personOne = Individual("@I1@")
        personOne.birth = datetime(datetime.today().year,datetime.today().month,30)
        personOne.death = datetime(2016,2,29)
        self.assertTrue(False == reject_invalid_dates(personOne))
                   
        
        


    
   
if __name__ == '__main__':
        unittest.main()
        
