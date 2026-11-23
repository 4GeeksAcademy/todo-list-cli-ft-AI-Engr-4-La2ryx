"""
Todo List — Interactive menu-driven task manager with file persistence.

Tasks now support:
  - Title
  - Priority (1–4, where 1 is highest)
  - Done / undone status
  - Edit title

Usage:
    python app.py

Menu:
    1. Add a task
    2. List tasks
    3. Delete a task
    4. Toggle done/undone
    5. Edit a task
    6. Save todos to file
    7. Load todos from file
    8. Exit
"""

import sys
import os

CSV_FILE = "todos.csv"

# In-memory task list — each task is a dict: {"title": str, "priority": int, "done": bool}
todos = []


# ── Helper ───────────────────────────────────────────────────


def _make_task(title, priority=2):
    """Return a new task dict."""
    return {"title": title, "priority": max(1, min(4, priority)), "done": False}


# ── Core functions ──────────────────────────────────────────


def add_one_task(title, priority=2):
    """Add a task with the given title and priority."""
    todos.append(_make_task(title, priority))
    print(f"Task added: \"{title}\" (priority {priority})")


def print_list():
    """Display all tasks with their number, priority, and status."""
    if not todos:
        print("No pending tasks. 🎉")
        return
    print("Tasks:")
    for i, t in enumerate(todos, start=1):
        status = "✓" if t["done"] else " "
        pri = t["priority"]
        print(f"  {i}. [{status}] (P{pri}) {t['title']}")


def delete_task(position):
    """Delete a task by its 1-based position."""
    if not todos:
        print("Error: There are no tasks to delete.", file=sys.stderr)
        return
    if position < 1 or position > len(todos):
        print(f"Error: Position {position} is out of range. "
              f"Valid positions are 1–{len(todos)}.", file=sys.stderr)
        return
    removed = todos.pop(position - 1)
    print(f"Task deleted: \"{removed['title']}\"")


def toggle_task(position):
    """Toggle the done status of a task by its 1-based position."""
    if not todos:
        print("Error: There are no tasks.", file=sys.stderr)
        return
    if position < 1 or position > len(todos):
        print(f"Error: Position {position} is out of range.", file=sys.stderr)
        return
    t = todos[position - 1]
    t["done"] = not t["done"]
    status = "done" if t["done"] else "undone"
    print(f"Task \"{t['title']}\" marked as {status}.")


def edit_task(position, new_title, new_priority=None):
    """Edit the title and optionally the priority of a task."""
    if not todos:
        print("Error: There are no tasks.", file=sys.stderr)
        return
    if position < 1 or position > len(todos):
        print(f"Error: Position {position} is out of range.", file=sys.stderr)
        return
    t = todos[position - 1]
    old_title = t["title"]
    t["title"] = new_title
    if new_priority is not None:
        t["priority"] = max(1, min(4, new_priority))
    print(f"Task updated: \"{old_title}\" → \"{t['title']}\"")


def save_todos():
    """Save the in-memory task list to the CSV file (title,priority,done)."""
    try:
        with open(CSV_FILE, "w") as f:
            for t in todos:
                f.write(f"{t['title']}|{t['priority']}|{int(t['done'])}\n")
        print(f"Saved {len(todos)} task(s) to {CSV_FILE}.")
    except (IOError, OSError):
        print("Error: Could not write to the tasks file.", file=sys.stderr)


def load_todos():
    """Load tasks from the CSV file (title|priority|done format)."""
    global todos
    if not os.path.exists(CSV_FILE):
        print(f"No save file found ({CSV_FILE}). Starting with an empty list.")
        return
    try:
        tasks = []
        with open(CSV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                title = parts[0]
                priority = int(parts[1]) if len(parts) > 1 else 2
                done = bool(int(parts[2])) if len(parts) > 2 else False
                tasks.append({"title": title, "priority": priority, "done": done})
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
    print("  4. Toggle done/undone")
    print("  5. Edit a task")
    print("  6. Save todos to file")
    print("  7. Load todos from file")
    print("  8. Exit")
    print("=" * 40)


def main():
    """Run the interactive todo list menu loop."""
    while True:
        print_menu()
        try:
            choice = input("Enter your choice (1–8): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)

        if choice == "1":
            title = input("Task title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.", file=sys.stderr)
                continue
            pri_str = input("Priority (1-4, default 2): ").strip()
            priority = int(pri_str) if pri_str.isdigit() else 2
            add_one_task(title, priority)

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
            if not todos:
                print("Error: There are no tasks.", file=sys.stderr)
                continue
            print_list()
            print("  (Enter 0 to go back)")
            try:
                pos = int(input("Enter the position to toggle: ").strip())
            except ValueError:
                print("Error: Position must be a number.", file=sys.stderr)
                continue
            if pos == 0:
                continue
            toggle_task(pos)

        elif choice == "5":
            if not todos:
                print("Error: There are no tasks.", file=sys.stderr)
                continue
            print_list()
            print("  (Enter 0 to go back)")
            try:
                pos = int(input("Enter the position to edit: ").strip())
            except ValueError:
                print("Error: Position must be a number.", file=sys.stderr)
                continue
            if pos == 0:
                continue
            new_title = input("New title: ").strip()
            if not new_title:
                print("Error: Title cannot be empty.", file=sys.stderr)
                continue
            pri_str = input("New priority (1-4, press Enter to keep): ").strip()
            new_pri = int(pri_str) if pri_str.isdigit() else None
            edit_task(pos, new_title, new_pri)

        elif choice == "6":
            save_todos()

        elif choice == "7":
            load_todos()

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Error: Invalid choice. Please enter a number from 1 to 8.",
                  file=sys.stderr)


if __name__ == "__main__":
    main()

