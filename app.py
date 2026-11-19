"""
Todo List CLI — A lightweight command-line tool for managing daily tasks.

Usage:
    python app.py add <task_title>    Add a new task
    python app.py list                Show all pending tasks
    python app.py delete <position>   Delete a task by its position number
    python app.py --help              Show this help message
"""

import sys
import os

CSV_FILE = "todos.csv"


def load_tasks():
    """Load tasks from the CSV file. Returns a list of task titles."""
    tasks = []
    if not os.path.exists(CSV_FILE):
        return tasks
    try:
        with open(CSV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    tasks.append(line)
    except (IOError, OSError):
        print("Error: Could not read the tasks file.", file=sys.stderr)
        sys.exit(1)
    return tasks


def save_tasks(tasks):
    """Save a list of task titles to the CSV file (one per line)."""
    try:
        with open(CSV_FILE, "w") as f:
            for task in tasks:
                f.write(task + "\n")
    except (IOError, OSError):
        print("Error: Could not write to the tasks file.", file=sys.stderr)
        sys.exit(1)


def add_task(title):
    """Add a new task with the given title."""
    tasks = load_tasks()
    tasks.append(title)
    save_tasks(tasks)
    print(f"Task added: \"{title}\"")


def list_tasks():
    """Display all pending tasks with their numeric position."""
    tasks = load_tasks()
    if not tasks:
        print("No pending tasks. 🎉")
        return
    print("Pending tasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"  {i}. {task}")


def delete_task(position):
    """Delete a task by its 1-based position in the list."""
    tasks = load_tasks()
    if not tasks:
        print("Error: There are no tasks to delete.", file=sys.stderr)
        sys.exit(1)
    if position < 1 or position > len(tasks):
        print(f"Error: Position {position} is out of range. ", end="", file=sys.stderr)
        print(f"Valid positions are 1–{len(tasks)}.", file=sys.stderr)
        sys.exit(1)
    removed = tasks.pop(position - 1)
    save_tasks(tasks)
    print(f"Task deleted: \"{removed}\"")


def print_help():
    print(__doc__.strip())


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print_help()
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task title.", file=sys.stderr)
            print("Usage: python app.py add \"<task_title>\"", file=sys.stderr)
            sys.exit(1)
        add_task(sys.argv[2])

    elif command == "list":
        list_tasks()

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a position number.", file=sys.stderr)
            print("Usage: python app.py delete <position>", file=sys.stderr)
            sys.exit(1)
        try:
            position = int(sys.argv[2])
        except ValueError:
            print("Error: Position must be a number.", file=sys.stderr)
            sys.exit(1)
        delete_task(position)

    else:
        print(f"Error: Unknown command \"{command}\".", file=sys.stderr)
        print("Run 'python app.py --help' to see available commands.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()