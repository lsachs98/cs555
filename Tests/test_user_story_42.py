import unittest
from parse_gedcom import *


class TestUserStory42(unittest.TestCase):
    def setUp(self):
        person = Individual("I1")
        person.name = "Test /Person/"
        individuals.append(person)

    def tearDown(self):
        individuals.clear()

    def test_valid_upcoming_birthday(self):
        get_individual("I1").birth = datetime.today().date() + timedelta(days=1)
        table = []
        reject_illegitimate_birthdays(table)
        self.assertTrue(table[0][3])

    def test_valid_passed_birthday(self):
        get_individual("I1").birth = datetime.today().date() - timedelta(days=1)
        table = []
        reject_illegitimate_birthdays(table)
        self.assertTrue(table[0][3])

    def test_invalid_upcoming_birthday(self):
        get_individual("I1").birth = datetime(datetime.today().year, datetime.today().month, 30).date()
        table = []
        reject_illegitimate_birthdays(table)
        self.assertFalse(table[0][3])

    def test_invalid_passed_birthday(self):
        get_individual("I1").birth = datetime(datetime.today().year, (datetime.today().month + 11) % 12, 30).date()
        table = []
        reject_illegitimate_birthdays(table)
        self.assertTrue(table[0][3])

    def test_no_dates(self):
        get_individual("I1").birth = None
        table = []
        reject_illegitimate_birthdays(table)
        self.assertTrue(table[0][3])

    def test_leap_year_and_mix_validity(self):
        get_individual("I1").birth = datetime(datetime.today().year, datetime.today().month, 30).date()
        get_individual("I1").death = datetime(2016, 2, 29).date()
        table = []
        reject_illegitimate_birthdays(table)
        self.assertFalse(table[0][3])


if __name__ == '__main__':
    unittest.main(verbosity=2)