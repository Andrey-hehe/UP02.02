import unittest
from difflib import SequenceMatcher


class TestDiff(unittest.TestCase):
    def test_identical_text(self):
        a = "Hello"
        b = "Hello"

        matcher = SequenceMatcher(None, a, b)

        self.assertEqual(matcher.ratio(), 1.0)

    def test_different_text(self):
        a = "Hello"
        b = "World"

        matcher = SequenceMatcher(None, a, b)

        self.assertLess(matcher.ratio(), 1.0)


if __name__ == "__main__":
    unittest.main()
