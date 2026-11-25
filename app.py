"""
Todo List — Interactive menu-driven task manager with file persistence.

The five required module-level functions:
    - add_one_task(title)   — add a task to the shared in-memory list
    - print_list()          — display all tasks with 1-based numbering
    - delete_task(position) — remove a task by its 1-based position
    - save_todos()          — persist the list to a CSV file
    - load_todos()          — restore the list from a CSV file

Usage:
    python app.py

Menu:
    1. Add a task
    2. List tasks
    3. Delete a task
    4. Save todos to file
    5. Load todos from file
    6. Exit
"""

import sys
import os

CSV_FILE = "todos.csv"

# In-memory task list — a list of plain strings, one per task title.
todos = []


# ── Core functions ──────────────────────────────────────────


def add_one_task(title):
    """Add a task (plain string) to the shared in-memory list."""
    todos.append(title)
    print(f"Task added: \"{title}\"")


def print_list():
    """Display all tasks with their 1-based position number."""
    if not todos:
        print("No pending tasks. 🎉")
        return
    print("Pending tasks:")
    for i, t in enumerate(todos, start=1):
        print(f"  {i}. {t}")


def delete_task(position):
    """Delete a task by its 1-based position. Prints an error on failure."""
    if not todos:
        print("Error: There are no tasks to delete.", file=sys.stderr)
        return
    if position < 1 or position > len(todos):
        print(f"Error: Position {position} is out of range. "
              f"Valid positions are 1–{len(todos)}.", file=sys.stderr)
        return
    removed = todos.pop(position - 1)
    print(f"Task deleted: \"{removed}\"")


def save_todos():
    """Save the in-memory task list to the CSV file (one title per line)."""
    try:
        with open(CSV_FILE, "w") as f:
            for t in todos:
                f.write(f"{t}\n")
        print(f"Saved {len(todos)} task(s) to {CSV_FILE}.")
    except (IOError, OSError):
        print("Error: Could not write to the tasks file.", file=sys.stderr)


def load_todos():
    """Load tasks from the CSV file into the in-memory list."""
    global todos
    if not os.path.exists(CSV_FILE):
        print(f"No save file found ({CSV_FILE}). Starting with an empty list.")
        return
    try:
        tasks = []
        with open(CSV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    tasks.append(line)
        todos = tasks
        print(f"Loaded {len(todos)} task(s) from {CSV_FILE}.")
    except (IOError, OSError):
        print("Error: Could not read the tasks file.", file=sys.stderr)


# ── Interactive menu ─────────────────────────────────────────


def print_menu():
    """Display the interactive menu options."""
    print("\n" + "=" * 40)
    print("           TODO LIST — MAIN MENU")
    print("=" * 40)
    print("  1. Add a task")
    print("  2. List tasks")
    print("  3. Delete a task")
    print("  4. Save todos to file")
    print("  5. Load todos from file")
    print("  6. Exit")
    print("=" * 40)


def main():
    """Run the interactive todo list menu loop."""
    while True:
        print_menu()
        try:
            choice = input("Enter your choice (1–6): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)

        if choice == "1":
            title = input("Task title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.", file=sys.stderr)
                continue
            add_one_task(title)

        elif choice == "2":
            print_list()

        elif choice == "3":
            if not todos:
                print("Error: There are no tasks to delete.", file=sys.stderr)
                continue
            print_list()
            print("  (Enter 0 to go back)")
            try:
                pos = int(input("Enter the position to delete: ").strip())
            except ValueError:
                print("Error: Position must be a number.", file=sys.stderr)
                continue
            if pos == 0:
                continue
            delete_task(pos)

        elif choice == "4":
            save_todos()

        elif choice == "5":
            load_todos()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Error: Invalid choice. Please enter a number from 1 to 6.",
                  file=sys.stderr)


if __name__ == "__main__":
    main()

