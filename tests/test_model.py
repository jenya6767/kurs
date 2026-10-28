import tempfile
import unittest
from pathlib import Path
from taskcore import TaskBoard, ValidationError

class TaskBoardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "tasks.json"
        self.board = TaskBoard(self.path)
    def tearDown(self):
        self.tmp.cleanup()
    def test_empty(self):
        self.assertEqual(self.board.summary(), (0, 0))
    def test_create(self):
        self.assertEqual(self.board.add("Кнопка").title, "Кнопка")
    def test_trim(self):
        self.assertEqual(self.board.add("   Макет  ").title, "Макет")
    def test_next_id(self):
        self.board.add("А")
        self.assertEqual(self.board.add("Б").id, 2)
    def test_blank_title(self):
        with self.assertRaises(ValidationError): self.board.add("   ")
    def test_long_title(self):
        with self.assertRaises(ValidationError): self.board.add("а" * 81)
    def test_non_string(self):
        with self.assertRaises(ValidationError): self.board.add(None)
    def test_toggle(self):
        t = self.board.add("А")
        self.assertTrue(self.board.toggle(t.id).done)
    def test_toggle_back(self):
        t = self.board.add("А")
        self.board.toggle(t.id)
        self.assertFalse(self.board.toggle(t.id).done)
    def test_toggle_missing(self):
        with self.assertRaises(ValidationError): self.board.toggle(8)
    def test_remove(self):
        t = self.board.add("А")
        self.board.remove(t.id)
        self.assertEqual(self.board.summary(), (0, 0))
    def test_remove_missing(self):
        with self.assertRaises(ValidationError): self.board.remove(8)
    def test_summary(self):
        first = self.board.add("А")
        self.board.add("Б")
        self.board.toggle(first.id)
        self.assertEqual(self.board.summary(), (2, 1))
    def test_reload(self):
        self.board.add("А")
        self.assertEqual(TaskBoard(self.path).tasks[0].title, "А")
    def test_no_file_in_memory(self):
        self.assertEqual(TaskBoard().add("А").id, 1)
    def test_invalid_json(self):
        self.path.write_text("{}", encoding="utf-8")
        with self.assertRaises(ValidationError): TaskBoard(self.path)
    def test_duplicate_ids(self):
        self.path.write_text('[{"id":1,"title":"A","done":false},{"id":1,"title":"B","done":false}]', encoding="utf-8")
        with self.assertRaises(ValidationError): TaskBoard(self.path)

if __name__ == "__main__": unittest.main()
