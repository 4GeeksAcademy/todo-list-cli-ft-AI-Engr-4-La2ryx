# Todo List CLI (Python)

A simple command-line Todo List application built with Python that allows users to create, view, delete, save, and load tasks from a CSV file via an interactive menu.

## Features

- Interactive 1–6 numbered menu
- Add new tasks
- View all tasks with numbered positions
- Delete tasks by number
- Save tasks to a CSV file
- Load tasks from a CSV file
- Persistent storage between program runs
- Flask web server (localhost:3000)

## Technologies Used

- Python 3
- File handling (CSV persistence)
- Interactive CLI menu
- Flask web interface (optional)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/La2ryx/todo-list-cli-ft-AI-Engr-4.git
```

2. Navigate to the project directory:

```bash
cd todo-list-cli-ft-AI-Engr-4
```

3. Run the application:

```bash
python app.py
```

## Usage

Run the program and follow the interactive menu:

```
===================================
        TODO LIST — MAIN MENU
===================================
  1. Add a task
  2. List tasks
  3. Delete a task
  4. Save todos to file
  5. Load todos from file
  6. Exit
===================================
```

### Add a Task (option 1)

```
Task title: Buy groceries
Task added: "Buy groceries"
```

### View All Tasks (option 2)

```
Pending tasks:
  1. Buy groceries
  2. Finish Python project
  3. Study for exam
```

### Delete a Task (option 3)

Displays current tasks, then prompts for the position number to delete.

### Save / Load (options 4 & 5)

Persist the in-memory list to `todos.csv` or restore from it.

### Web Server (optional)

```bash
python server.py
```

Then open `http://localhost:3000` in your browser.

## Project Structure

```
.
├── app.py          # Interactive CLI application (5 required functions + menu)
├── test.py         # Unit tests (17 tests)
├── server.py       # Flask web server (optional)
├── main.py         # Minimal hello-world script (starter template)
├── learn.json      # Project metadata
├── .gitignore      # Ignores __pycache__ and todos.csv
├── README.md       # This file
└── README.es.md    # Spanish translation
```

## Testing

Run the test suite with:

```bash
python test.py
```

All 17 tests should pass, covering:

| Test | Coverage |
|------|----------|
| `add_one_task` | Single, multiple, special characters |
| `print_list` | Empty list, populated list |
| `delete_task` | First, middle, last, only, out-of-range, empty |
| `save_todos` + `load_todos` | Round-trip, single-task, empty, missing-file, compose |

## What I Learned

During this project, I practiced:

- Python functions operating on a shared in-memory list
- Interactive CLI menu patterns
- Reading and writing CSV files
- Unit testing with `unittest`
- Web server integration
- Command-line application development
- Error handling and user input validation
- Git and GitHub workflow

## Future Improvements

- Task completion status
- Task priorities
- Due dates
- Search and filter tasks
- Colored terminal output
- Unit test coverage

## Author

**Larry**

GitHub: [https://github.com/La2ryx](https://github.com/La2ryx)
