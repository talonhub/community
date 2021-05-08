"""
Will run all the tests defined in the knausj repository. To use install python3.9 on your
host machine and run `python run_tests.py`.
"""

import os
import sys
import unittest


if __name__ == "__main__":
    # Code in this statement doesn't run in the Talon environment.

    curr_dir = os.path.dirname(__file__)

    # Add in our talon stubs to the python search path
    sys.path.append(os.path.join(curr_dir, "tests", "stubs"))
    # And also add the current directory so we can do stuff like
    # `import code.formatters` in tests.
    sys.path.append(curr_dir)

    # Now execute our tests
    test_absolute_path = os.path.join(curr_dir, "tests")
    tests = unittest.TestLoader().discover(test_absolute_path)
    unittest.TextTestRunner().run(tests)
