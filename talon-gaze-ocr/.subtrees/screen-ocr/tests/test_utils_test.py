import unittest

import test_utils


class TestUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_cost(self):
        gt = "test"
        self.assertLess(test_utils.cost("test", gt), test_utils.cost("text", gt))

        self.assertLess(
            test_utils.cost("ignore some test case ignore", gt),
            test_utils.cost("top elf saw top", gt),
        )

        self.assertLess(
            test_utils.cost("t asdfasdfasdf est case ignore", gt),
            test_utils.cost("asdfasdfasdf st case ignore", gt),
        )


if __name__ == "__main__":
    unittest.main()
