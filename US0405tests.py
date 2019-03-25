import unittest
import parse_gedcom
files = (parse_gedcom.read_file is " ")

class TestSprints(unittest.TestCase):
    def testUS04(self):
        self.assertNotEqual(parse_gedcom.user_story_04,  'T')
    def testUS05(self):
        self.assertNotEqual(parse_gedcom.user_story_05, 'T')
    

if __name__ == '__main__':
    unittest.main()
