"""
Flask web server for the Todo List app.
Provides a browser-based interface backed by app.py's in-memory list.
"""

try:
    from flask import Flask, request, redirect, url_for, render_template_string
except ImportError:
    print("You don't have Flask installed, run `$ pip3 install flask` and try again")
    exit(1)

import os
import app as todo_app

server = Flask(__name__)

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo List</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #f0f2f5; display: flex; justify-content: center; padding: 2rem 1rem; }}
        .container {{ max-width: 650px; width: 100%; background: white; border-radius: 12px;
                      box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 2rem; }}
        h1 {{ text-align: center; color: #1a1a2e; margin-bottom: 1.5rem; font-size: 1.8rem; }}
        .form-row {{ display: flex; gap: 0.5rem; margin-bottom: 0.75rem; }}
        .form-row input[type=text] {{ flex: 1; padding: 0.6rem 1rem;
               border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; outline: none; }}
        .form-row input[type=text]:focus {{ border-color: #4361ee; }}
        .btn {{ padding: 0.6rem 1.2rem; border: none; border-radius: 8px; font-size: 1rem;
                cursor: pointer; color: white; transition: background 0.2s; text-decoration: none;
                display: inline-block; }}
        .btn-add {{ background: #4361ee; }} .btn-add:hover {{ background: #3a56d4; }}
        .btn-del {{ background: #e63946; padding: 0.3rem 0.7rem; font-size: 0.85rem; }}
        .btn-del:hover {{ background: #c1121f; }}
        .btn-save {{ background: #2a9d8f; }} .btn-save:hover {{ background: #21867a; }}
        .btn-load {{ background: #e9c46a; color: #333; }} .btn-load:hover {{ background: #d4b05a; }}
        .task-list {{ list-style: none; margin: 1rem 0; }}
        .task-item {{ display: flex; justify-content: space-between; align-items: center;
                      padding: 0.6rem 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.5rem;
                      border-left: 4px solid #4361ee; }}
        .task-item .left {{ display: flex; align-items: center; gap: 0.5rem; }}
        .task-item .num {{ color: #888; font-weight: 600; min-width: 1.5rem; }}
        .task-item .title {{ word-break: break-word; }}
        .task-item .actions {{ display: flex; gap: 0.35rem; }}
        .empty-msg {{ text-align: center; color: #888; padding: 2rem; font-size: 1.1rem; }}
        .msg {{ padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.95rem; }}
        .msg-success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
        .msg-error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
        .actions-bar {{ display: flex; gap: 0.5rem; margin-top: 1rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Todo List</h1>
        {message_html}

        <form method="POST" action="/add" class="form-row">
            <input type="text" name="title" placeholder="Enter a new task..." required>
            <button type="submit" class="btn btn-add">Add</button>
        </form>

        {tasks_html}

        <div class="actions-bar">
            <a href="/save" class="btn btn-save">💾 Save to file</a>
            <a href="/load" class="btn btn-load">📂 Load from file</a>
        </div>
    </div>
</body>
</html>"""


def render_page(message="", msg_type="success"):
    """Render the todo list as an HTML page."""
    if todo_app.todos:
        items = []
        for i, t in enumerate(todo_app.todos, start=1):
            delete_url = url_for('delete', pos=i)
            items.append(
                f'<li class="task-item">'
                f'  <div class="left">'
                f'    <span class="num">{i}.</span>'
                f'    <span class="title">{t}</span>'
                f'  </div>'
                f'  <div class="actions">'
                f'    <a href="{delete_url}" class="btn btn-del">✕</a>'
                f'  </div>'
                f'</li>\n'
            )
        tasks_html = f'<ul class="task-list">{"".join(items)}</ul>'
    else:
        tasks_html = '<p class="empty-msg">No pending tasks. 🎉</p>'

    if message:
        msg_html = f'<div class="msg msg-{msg_type}">{message}</div>'
    else:
        msg_html = ""

    return HTML_TEMPLATE.format(message_html=msg_html, tasks_html=tasks_html)


@server.route('/', methods=['GET'])
def index():
    return render_page()


@server.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if not title:
        return render_page("Error: Task title cannot be empty.", "error")
    todo_app.add_one_task(title)
    return redirect(url_for('index'))


@server.route('/delete/<int:pos>', methods=['GET'])
def delete(pos):
    if not todo_app.todos:
        return render_page("Error: There are no tasks to delete.", "error")
    if pos < 1 or pos > len(todo_app.todos):
        return render_page(f"Error: Position {pos} is out of range.", "error")
    todo_app.delete_task(pos)
    return redirect(url_for('index'))


@server.route('/save', methods=['GET'])
def save():
    todo_app.save_todos()
    return redirect(url_for('index'))


@server.route('/load', methods=['GET'])
def load():
    todo_app.load_todos()
    return redirect(url_for('index'))


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=3000, debug=True)
