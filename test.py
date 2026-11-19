"""
Tests for the Todo List CLI (app.py).

Run with:
    python test.py          # quick test runner
    python -m pytest test.py   # or use pytest
"""

import os
import sys
import unittest
import tempfile
import subprocess

# Ensure we can import app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app


class TestTodoCLI(unittest.TestCase):
    """Unit tests for Todo List CLI functions."""

    def setUp(self):
        """Create a temporary directory and switch to it for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.orig_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        # Ensure we start with no todos.csv
        self._remove_csv()

    def tearDown(self):
        """Clean up the temporary directory and restore cwd."""
        self._remove_csv()  # remove CSV while still in temp dir
        os.chdir(self.orig_cwd)
        os.rmdir(self.temp_dir)

    def _remove_csv(self):
        csv_path = os.path.join(os.getcwd(), app.CSV_FILE)
        if os.path.exists(csv_path):
            os.remove(csv_path)

    # ── load / save ──────────────────────────────────────────────

    def test_empty_list_when_no_csv(self):
        """load_tasks returns an empty list when no CSV file exists."""
        self.assertEqual(app.load_tasks(), [])

    def test_save_and_load_tasks(self):
        """Tasks saved to CSV are loaded back correctly."""
        expected = ["Buy groceries", "Write report", "Call client"]
        app.save_tasks(expected)
        loaded = app.load_tasks()
        self.assertEqual(loaded, expected)

    def test_save_and_load_single_task(self):
        """A single task round-trips correctly."""
        app.save_tasks(["Take out the trash"])
        self.assertEqual(app.load_tasks(), ["Take out the trash"])

    def test_save_and_load_empty(self):
        """Saving an empty list produces an empty file and loads to empty list."""
        app.save_tasks([])
        self.assertEqual(app.load_tasks(), [])

    # ── add ──────────────────────────────────────────────────────

    def test_add_one_task(self):
        """Adding one task stores it in the CSV."""
        app.add_task("Buy milk")
        self.assertEqual(app.load_tasks(), ["Buy milk"])

    def test_add_multiple_tasks(self):
        """Adding multiple tasks appends them in order."""
        app.add_task("First")
        app.add_task("Second")
        app.add_task("Third")
        self.assertEqual(app.load_tasks(), ["First", "Second", "Third"])

    def test_add_task_with_special_characters(self):
        """Tasks with punctuation and spaces are stored as-is."""
        app.add_task("Fix server #3 — ASAP!")
        self.assertEqual(app.load_tasks(), ["Fix server #3 — ASAP!"])

    # ── list ─────────────────────────────────────────────────────

    def test_list_empty(self):
        """list_tasks runs without error when there are no tasks."""
        # Should just print "No pending tasks." – no crash
        app.list_tasks()

    def test_list_with_tasks(self):
        """list_tasks prints tasks with 1-based numbering."""
        app.save_tasks(["Alpha", "Beta", "Gamma"])
        # If it doesn't crash, the output is printed to stdout
        app.list_tasks()

    # ── delete ───────────────────────────────────────────────────

    def test_delete_first_task(self):
        """Deleting the first task removes it and keeps the rest."""
        app.save_tasks(["A", "B", "C"])
        app.delete_task(1)
        self.assertEqual(app.load_tasks(), ["B", "C"])

    def test_delete_last_task(self):
        """Deleting the last task removes it and keeps the rest."""
        app.save_tasks(["A", "B", "C"])
        app.delete_task(3)
        self.assertEqual(app.load_tasks(), ["A", "B"])

    def test_delete_middle_task(self):
        """Deleting a middle task shifts later items up."""
        app.save_tasks(["A", "B", "C", "D"])
        app.delete_task(2)
        self.assertEqual(app.load_tasks(), ["A", "C", "D"])

    def test_delete_only_task(self):
        """Deleting the only task leaves the list empty."""
        app.save_tasks(["Solo"])
        app.delete_task(1)
        self.assertEqual(app.load_tasks(), [])

    def test_delete_out_of_range_low(self):
        """Deleting position < 1 raises SystemExit."""
        app.save_tasks(["A", "B"])
        with self.assertRaises(SystemExit):
            app.delete_task(0)

    def test_delete_out_of_range_high(self):
        """Deleting position > list length raises SystemExit."""
        app.save_tasks(["A", "B"])
        with self.assertRaises(SystemExit):
            app.delete_task(3)

    def test_delete_from_empty(self):
        """Deleting from empty list raises SystemExit."""
        app.save_tasks([])
        with self.assertRaises(SystemExit):
            app.delete_task(1)

    # ── persistence ──────────────────────────────────────────────

    def test_persistence_across_operations(self):
        """Adding and deleting persists to CSV between operations."""
        app.add_task("Task 1")
        app.add_task("Task 2")
        app.add_task("Task 3")
        self.assertEqual(app.load_tasks(), ["Task 1", "Task 2", "Task 3"])

        app.delete_task(2)
        self.assertEqual(app.load_tasks(), ["Task 1", "Task 3"])

        app.add_task("Task 4")
        self.assertEqual(app.load_tasks(), ["Task 1", "Task 3", "Task 4"])


class TestTodoCLIFromShell(unittest.TestCase):
    """Integration tests that run app.py as a subprocess (CLI level)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.orig_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        self.app_path = os.path.join(self.orig_cwd, "app.py")

    def tearDown(self):
        os.chdir(self.orig_cwd)
        csv_path = os.path.join(self.temp_dir, app.CSV_FILE)
        if os.path.exists(csv_path):
            os.remove(csv_path)
        os.rmdir(self.temp_dir)

    def _run(self, *args):
        """Run app.py with the given arguments and return (returncode, stdout, stderr)."""
        result = subprocess.run(
            [sys.executable, self.app_path, *args],
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout, result.stderr

    def test_cli_add(self):
        """app.py add <title> creates a task."""
        rc, out, err = self._run("add", "Test task")
        self.assertEqual(rc, 0)

    def test_cli_list_empty(self):
        """app.py list on empty list prints friendly message."""
        rc, out, err = self._run("list")
        self.assertEqual(rc, 0)
        self.assertIn("No pending", out)

    def test_cli_add_and_list(self):
        """Adding a task then listing shows it."""
        self._run("add", "My task")
        rc, out, err = self._run("list")
        self.assertEqual(rc, 0)
        self.assertIn("My task", out)

    def test_cli_delete(self):
        """app.py delete <pos> removes the task."""
        self._run("add", "Task to delete")
        rc, out, err = self._run("delete", "1")
        self.assertEqual(rc, 0)
        # Listing should show no pending tasks
        rc2, out2, err2 = self._run("list")
        self.assertIn("No pending", out2)

    def test_cli_delete_invalid_position(self):
        """app.py delete with invalid position exits with error."""
        self._run("add", "Some task")
        rc, out, err = self._run("delete", "999")
        self.assertNotEqual(rc, 0)
        self.assertIn("out of range", err)

    def test_cli_delete_non_numeric(self):
        """app.py delete with non-numeric position exits with error."""
        rc, out, err = self._run("delete", "abc")
        self.assertNotEqual(rc, 0)
        self.assertIn("number", err)

    def test_cli_unknown_command(self):
        """app.py with an unknown command exits with error."""
        rc, out, err = self._run("unknown")
        self.assertNotEqual(rc, 0)
        self.assertIn("Unknown", err)

    def test_cli_no_args_shows_help(self):
        """app.py with no arguments prints help and exits successfully."""
        rc, out, err = self._run()
        self.assertEqual(rc, 0)
        self.assertIn("Usage", out)

    def test_cli_help_flag(self):
        """app.py --help prints help."""
        rc, out, err = self._run("--help")
        self.assertEqual(rc, 0)
        self.assertIn("Usage", out)

    def test_persistence_after_second_run(self):
        """Tasks survive a restart — second process loads the CSV."""
        self._run("add", "Persistent task")
        # Simulate a new process (same dir, different Python invocation)
        rc, out, err = self._run("list")
        self.assertIn("Persistent task", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)