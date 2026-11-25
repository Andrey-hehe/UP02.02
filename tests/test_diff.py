import tempfile
import unittest
from pathlib import Path

from src.main import compare_json, get_changes


class TestDiff(unittest.TestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def create_file(self, name, content):
        path = self.folder / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_text_changes(self):
        first = self.create_file("first.txt", "removed\nkeep one\nold\nkeep two")
        second = self.create_file("second.txt", "keep one\nnew\nkeep two\nadded")

        self.assertEqual(
            get_changes(first, second),
            {
                "added": ["added"],
                "deleted": ["removed"],
                "modified": [{"old": ["old"], "new": ["new"]}],
            },
        )

    def test_nested_json_changes(self):
        first = self.create_file("first.json", '{"user":{"name":"Alex","age":20}}')
        second = self.create_file(
            "second.json", '{"user":{"name":"Sam","active":true}}'
        )

        self.assertEqual(
            compare_json(first, second),
            {
                "added": {"user.active": True},
                "deleted": {"user.age": 20},
                "modified": {"user.name": {"old": "Alex", "new": "Sam"}},
            },
        )


if __name__ == "__main__":
    unittest.main()
