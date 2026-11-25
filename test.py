"""
Official tests for the Todo List CLI (app.py).

The five required module-level functions tested:
    - add_one_task(title)
    - print_list()
    - delete_task(position)
    - save_todos()
    - load_todos()

The in-memory list is `app.todos` — a list of plain strings.

Run with:
    python test.py              # quick test runner
    python -m pytest test.py    # or use pytest
"""

import os
import sys
import unittest
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app


class TestTodoFunctions(unittest.TestCase):
    """Unit tests for the five required todo functions on the shared list."""

    def setUp(self):
        """Clear the in-memory list and work in a temp directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.orig_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        app.todos.clear()
        self._remove_csv()

    def tearDown(self):
        self._remove_csv()
        os.chdir(self.orig_cwd)
        os.rmdir(self.temp_dir)

    def _remove_csv(self):
        csv_path = os.path.join(os.getcwd(), app.CSV_FILE)
        if os.path.exists(csv_path):
            os.remove(csv_path)

    # ── add_one_task ─────────────────────────────────────────

    def test_add_one_task(self):
        """add_one_task appends to the in-memory list."""
        app.add_one_task("Buy milk")
        self.assertEqual(app.todos, ["Buy milk"])

    def test_add_multiple_tasks(self):
        """add_one_task appends multiple tasks in order."""
        app.add_one_task("First")
        app.add_one_task("Second")
        app.add_one_task("Third")
        self.assertEqual(app.todos, ["First", "Second", "Third"])

    def test_add_task_with_special_characters(self):
        """Tasks with punctuation and spaces are stored as-is."""
        app.add_one_task("Fix server #3 — ASAP!")
        self.assertEqual(app.todos, ["Fix server #3 — ASAP!"])

    # ── print_list ───────────────────────────────────────────

    def test_print_list_empty(self):
        """print_list runs without error when there are no tasks."""
        app.print_list()  # should just print — no crash

    def test_print_list_with_tasks(self):
        """print_list prints tasks with 1-based numbering."""
        app.todos.extend(["Alpha", "Beta", "Gamma"])
        app.print_list()  # no crash expected

    # ── delete_task ──────────────────────────────────────────

    def test_delete_first_task(self):
        """Deleting the first task removes it and keeps the rest."""
        app.todos.extend(["A", "B", "C"])
        app.delete_task(1)
        self.assertEqual(app.todos, ["B", "C"])

    def test_delete_last_task(self):
        """Deleting the last task removes it."""
        app.todos.extend(["A", "B", "C"])
        app.delete_task(3)
        self.assertEqual(app.todos, ["A", "B"])

    def test_delete_middle_task(self):
        """Deleting a middle task shifts later items up."""
        app.todos.extend(["A", "B", "C", "D"])
        app.delete_task(2)
        self.assertEqual(app.todos, ["A", "C", "D"])

    def test_delete_only_task(self):
        """Deleting the only task leaves the list empty."""
        app.todos.append("Solo")
        app.delete_task(1)
        self.assertEqual(app.todos, [])

    def test_delete_out_of_range_low(self):
        """Deleting position < 1 prints error but does NOT crash."""
        app.todos.extend(["A", "B"])
        app.delete_task(0)  # no exception expected
        self.assertEqual(app.todos, ["A", "B"])

    def test_delete_out_of_range_high(self):
        """Deleting position > list length prints error but does NOT crash."""
        app.todos.extend(["A", "B"])
        app.delete_task(3)
        self.assertEqual(app.todos, ["A", "B"])

    def test_delete_from_empty(self):
        """Deleting from empty list prints error but does NOT crash."""
        app.delete_task(1)  # no exception expected

    # ── save_todos + load_todos ──────────────────────────────

    def test_save_and_load_round_trip(self):
        """save_todos then load_todos restores the list from disk."""
        app.todos.extend(["Buy groceries", "Write report", "Call client"])
        app.save_todos()
        app.todos.clear()
        app.load_todos()
        self.assertEqual(app.todos, ["Buy groceries", "Write report", "Call client"])

    def test_save_and_load_single_task(self):
        """A single task round-trips correctly."""
        app.todos.append("Take out the trash")
        app.save_todos()
        app.todos.clear()
        app.load_todos()
        self.assertEqual(app.todos, ["Take out the trash"])

    def test_save_and_load_empty(self):
        """Saving an empty list then loading returns empty."""
        app.save_todos()
        app.todos.append("Stale")
        app.load_todos()
        self.assertEqual(app.todos, [])

    def test_load_when_no_csv(self):
        """load_todos leaves the list unchanged when no CSV exists."""
        app.todos.extend(["Keep me"])
        app.load_todos()
        self.assertEqual(app.todos, ["Keep me"])

    def test_persistence_across_operations(self):
        """Adding, saving, loading, deleting all compose correctly."""
        app.add_one_task("Task 1")
        app.add_one_task("Task 2")
        app.add_one_task("Task 3")
        app.save_todos()

        app.todos.clear()
        app.load_todos()
        self.assertEqual(app.todos, ["Task 1", "Task 2", "Task 3"])

        app.delete_task(2)
        self.assertEqual(app.todos, ["Task 1", "Task 3"])

        app.add_one_task("Task 4")
        self.assertEqual(app.todos, ["Task 1", "Task 3", "Task 4"])


if __name__ == "__main__":
    unittest.main(verbosity=2)