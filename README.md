# Todo List CLI (Python)

A simple command-line Todo List application built with Python that allows users to create, view, delete, save, and load tasks from a CSV file.

## Features

- Add new tasks
- View all tasks with numbered positions
- Delete tasks by number
- Save tasks to a CSV file
- Load tasks from a CSV file
- Persistent storage between program runs
- Simple command-line interface

## Technologies Used

- Python 3
- CSV module
- File handling
- Command-line arguments

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
python app.py --help
```

## Usage

### Add a Task

```bash
python app.py add "Buy groceries"
```

### View All Tasks

```bash
python app.py list
```

Example output:

```
Pending tasks:
  1. Buy groceries
  2. Finish Python project
  3. Study for exam
```

### Delete a Task

```bash
python app.py delete 2
```

### Persistence

Tasks are automatically saved to `todos.csv` and loaded back when you run the app again — no separate save/load commands needed.

## Project Structure

```
.
├── app.py
├── test.py
├── todos.csv
├── .gitignore
└── README.md
```

## Testing

Run the test suite with:

```bash
python test.py
```

## What I Learned

During this project, I practiced:

- Python functions
- Lists and data management
- Reading and writing CSV files
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
