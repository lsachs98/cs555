import unittest
from parse_gedcom import *


class TestUserStory38(unittest.TestCase):
    def setUp(self):
        person = Individual("I1")
        person.name = "Test /Person/"
        individuals.append(person)

    def tearDown(self):
        individuals.clear()

    def test_valid_upcoming_birthday(self):
        get_individual("I1").birth = datetime.today().date() + timedelta(days=1)
        table = []
        upcoming_birthdays(table)
        self.assertCountEqual([get_individual("I1").name], table[0][4].split("\n"))

    def test_valid_passed_birthday(self):
        get_individual("I1").birth = datetime.today().date() - timedelta(days=1)
        table = []
        upcoming_birthdays(table)
        self.assertFalse(table[0][4].split())

    def test_invalid_upcoming_birthday(self):
        get_individual("I1").birth = datetime(datetime.today().year, datetime.today().month, 30).date()
        table = []
        upcoming_birthdays(table)
        self.assertCountEqual([get_individual("I1").name], table[0][4].split("\n"))

    def test_invalid_passed_birthday(self):
        get_individual("I1").birth = datetime(datetime.today().year, (datetime.today().month + 11) % 12, 30).date()
        table = []
        upcoming_birthdays(table)
        self.assertFalse(table[0][4].split())

    def test_empty_file(self):
        individuals.clear()
        table = []
        upcoming_birthdays(table)
        self.assertFalse(table[0][4].split())


if __name__ == '__main__':
    unittest.main(verbosity=2)