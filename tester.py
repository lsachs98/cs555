import unittest

from Tests.test_user_story_09 import TestUserStory09
from Tests.test_user_story_11 import TestUserStory11
from Tests.test_user_story_12 import TestUserStory12
from Tests.test_user_story_13 import TestUserStory13
from Tests.test_user_story_17 import TestUserStory17
from Tests.test_user_story_18 import TestUserStory18


def test():
    loader = unittest.TestLoader()
    suites = [loader.loadTestsFromTestCase(TestUserStory09), loader.loadTestsFromTestCase(TestUserStory11),
              loader.loadTestsFromTestCase(TestUserStory12), loader.loadTestsFromTestCase(TestUserStory13),
              loader.loadTestsFromTestCase(TestUserStory17), loader.loadTestsFromTestCase(TestUserStory18)]

    tests = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    test()
