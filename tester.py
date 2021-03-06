import unittest

from Tests.test_user_story_09 import TestUserStory09
from Tests.test_user_story_11 import TestUserStory11
from Tests.test_user_story_12 import TestUserStory12
from Tests.test_user_story_13 import TestUserStory13
from Tests.test_user_story_15 import TestUserStory15
from Tests.test_user_story_16 import TestUserStory16
from Tests.test_user_story_17 import TestUserStory17
from Tests.test_user_story_18 import TestUserStory18
from Tests.test_user_story_28 import TestUserStory28
from Tests.test_user_story_29 import TestUserStory29
from Tests.test_user_story_30 import TestUserStory30
from Tests.test_user_story_31 import TestUserStory31
from Tests.test_user_story_35 import TestUserStory35
from Tests.test_user_story_36 import TestUserStory36
from Tests.test_user_story_38 import TestUserStory38
from Tests.test_user_story_42 import TestUserStory42


def test():
    loader = unittest.TestLoader()
    suites = [loader.loadTestsFromTestCase(TestUserStory09), loader.loadTestsFromTestCase(TestUserStory11),
              loader.loadTestsFromTestCase(TestUserStory12), loader.loadTestsFromTestCase(TestUserStory13),
              loader.loadTestsFromTestCase(TestUserStory15), loader.loadTestsFromTestCase(TestUserStory16),
              loader.loadTestsFromTestCase(TestUserStory17), loader.loadTestsFromTestCase(TestUserStory18),
              loader.loadTestsFromTestCase(TestUserStory28), loader.loadTestsFromTestCase(TestUserStory29),
              loader.loadTestsFromTestCase(TestUserStory30), loader.loadTestsFromTestCase(TestUserStory31),
              loader.loadTestsFromTestCase(TestUserStory35), loader.loadTestsFromTestCase(TestUserStory36),
              loader.loadTestsFromTestCase(TestUserStory38), loader.loadTestsFromTestCase(TestUserStory42)]

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))


if __name__ == '__main__':
    test()
