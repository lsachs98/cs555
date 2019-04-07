import unittest

from Tests.test_user_story_09 import TestUserStory09
from Tests.test_user_story_11 import TestUserStory11
from Tests.test_user_story_12 import TestUserStory12
from Tests.test_user_story_13 import TestUserStory13
from Tests.test_user_story_17 import TestUserStory17
from Tests.test_user_story_18 import TestUserStory18
from Tests.test_user_story_28 import TestUserStory28
from Tests.test_user_story_29 import TestUserStory29
from Tests.test_user_story_30 import TestUserStory30
from Tests.test_user_story_31 import TestUserStory31


def test():
    loader = unittest.TestLoader()
    suites = [loader.loadTestsFromTestCase(TestUserStory09), loader.loadTestsFromTestCase(TestUserStory11),
              loader.loadTestsFromTestCase(TestUserStory12), loader.loadTestsFromTestCase(TestUserStory13),
              loader.loadTestsFromTestCase(TestUserStory17), loader.loadTestsFromTestCase(TestUserStory18),
              loader.loadTestsFromTestCase(TestUserStory28), loader.loadTestsFromTestCase(TestUserStory29),
              loader.loadTestsFromTestCase(TestUserStory30), loader.loadTestsFromTestCase(TestUserStory31)]

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))


if __name__ == '__main__':
    test()
