import tempfile
import unittest
from pathlib import Path

from src.main import compare_files, compare_json, get_changes, read_file, save_report


class TestDiff(unittest.TestCase):
    def test_added_lines(self):
        first = self.create_file("first.txt", "Hello")
        second = self.create_file("second.txt", "Hello\nWorld")

        result = get_changes(first, second)

        self.assertEqual(result["added"], ["World"])

    def test_deleted_lines(self):
        first = self.create_file("first.txt", "Hello\nWorld")
        second = self.create_file("second.txt", "Hello")

        result = get_changes(first, second)

        self.assertEqual(result["deleted"], ["World"])

    def test_modified_lines(self):
        first = self.create_file("first.txt", "Hello")
        second = self.create_file("second.txt", "Goodbye")

        result = get_changes(first, second)

        self.assertEqual(result["modified"], [{"old": ["Hello"], "new": ["Goodbye"]}])

    def test_json_added_field(self):
        first = self.create_file("first.json", '{"name":"Alex"}')
        second = self.create_file("second.json", '{"name":"Alex","age":20}')

        result = compare_json(first, second)

        self.assertEqual(result["added"], {"age": 20})

    def test_json_deleted_field(self):
        first = self.create_file("first.json", '{"name":"Alex","age":20}')
        second = self.create_file("second.json", '{"name":"Alex"}')

        result = compare_json(first, second)

        self.assertEqual(result["deleted"], {"age": 20})

    def test_json_modified_field(self):
        first = self.create_file("first.json", '{"age":20}')
        second = self.create_file("second.json", '{"age":21}')

        result = compare_json(first, second)

        self.assertEqual(result["modified"], {"age": {"old": 20, "new": 21}})

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_file(self, name, content):
        path = self.folder / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_read_file(self):
        path = self.create_file("test.txt", "Привет, мир!")

        result = read_file(path)

        self.assertEqual(result, "Привет, мир!")

    def test_compare_files(self):
        first = self.create_file("first.txt", "Hello")
        second = self.create_file("second.txt", "World")

        result = compare_files(first, second)

        self.assertIn("Hello", result)
        self.assertIn("World", result)

    def test_save_report(self):
        path = self.folder / "report.html"

        save_report("<html>Test</html>", path)

        self.assertTrue(path.exists())
        self.assertEqual(path.read_text(encoding="utf-8"), "<html>Test</html>")

    def test_json_file(self):
        content = '{"name":"Alex","age":20}'
        path = self.create_file("test.json", content)

        result = read_file(path)

        self.assertIn('"name": "Alex"', result)
        self.assertIn('"age": 20', result)


if __name__ == "__main__":
    unittest.main()
