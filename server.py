try:
    from flask import Flask, request, redirect, url_for, render_template_string
except ImportError:
    print("You don't have Flask installed, run `$ pip3 install flask` and try again")
    exit(1)

import os
import app as todo_app

app = Flask(__name__)

# Priority label & colour mapping
PRIORITY_LABEL = {1: "🔴", 2: "🟡", 3: "🟢", 4: "🔵"}
PRIORITY_COLOR = {1: "#e63946", 2: "#e9c46a", 3: "#2a9d8f", 4: "#4361ee"}

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
        .form-row {{ display: flex; gap: 0.5rem; margin-bottom: 0.75rem; flex-wrap: wrap; }}
        .form-row input[type=text] {{ flex: 1; min-width: 180px; padding: 0.6rem 1rem;
               border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; outline: none; }}
        .form-row input[type=text]:focus {{ border-color: #4361ee; }}
        .form-row select {{ padding: 0.6rem 0.8rem; border: 2px solid #e0e0e0; border-radius: 8px;
              font-size: 1rem; outline: none; background: white; }}
        .btn {{ padding: 0.6rem 1.2rem; border: none; border-radius: 8px; font-size: 1rem;
                cursor: pointer; color: white; transition: background 0.2s; text-decoration: none;
                display: inline-block; }}
        .btn-add {{ background: #4361ee; }} .btn-add:hover {{ background: #3a56d4; }}
        .btn-del {{ background: #e63946; padding: 0.3rem 0.7rem; font-size: 0.85rem; }}
        .btn-del:hover {{ background: #c1121f; }}
        .btn-toggle {{ background: #6c757d; padding: 0.3rem 0.7rem; font-size: 0.85rem; }}
        .btn-toggle:hover {{ background: #5a6268; }}
        .btn-edit {{ background: #f4a261; padding: 0.3rem 0.7rem; font-size: 0.85rem; color: #333; }}
        .btn-edit:hover {{ background: #e08e4a; }}
        .btn-save {{ background: #2a9d8f; }} .btn-save:hover {{ background: #21867a; }}
        .btn-load {{ background: #e9c46a; color: #333; }} .btn-load:hover {{ background: #d4b05a; }}
        .btn-cancel {{ background: #adb5bd; }} .btn-cancel:hover {{ background: #8e959c; }}
        .task-list {{ list-style: none; margin: 1rem 0; }}
        .task-item {{ display: flex; justify-content: space-between; align-items: center;
                      padding: 0.6rem 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.5rem;
                      border-left: 4px solid #4361ee; transition: opacity 0.15s; }}
        .task-item.done {{ opacity: 0.55; border-left-color: #6c757d; }}
        .task-item .left {{ display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }}
        .task-item .num {{ color: #888; font-weight: 600; min-width: 1.5rem; }}
        .task-item .pri-tag {{ font-size: 0.75rem; font-weight: 700; padding: 0.1rem 0.45rem;
                               border-radius: 4px; color: white; }}
        .task-item .title {{ word-break: break-word; }}
        .task-item .title.done-text {{ text-decoration: line-through; color: #888; }}
        .task-item .actions {{ display: flex; gap: 0.35rem; }}
        .empty-msg {{ text-align: center; color: #888; padding: 2rem; font-size: 1.1rem; }}
        .msg {{ padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.95rem; }}
        .msg-success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
        .msg-error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
        .actions-bar {{ display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap; }}

        /* ── Inline edit form ── */
        .edit-form {{ display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; width: 100%; }}
        .edit-form input[type=text] {{ flex: 1; min-width: 140px; padding: 0.4rem 0.8rem;
               border: 2px solid #e0e0e0; border-radius: 6px; font-size: 0.95rem; outline: none; }}
        .edit-form input[type=text]:focus {{ border-color: #f4a261; }}
        .edit-form select {{ padding: 0.4rem 0.6rem; border: 2px solid #e0e0e0; border-radius: 6px;
              font-size: 0.95rem; background: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Todo List</h1>
        {message_html}

        <!-- Add form with priority selector -->
        <form method="POST" action="/add" class="form-row">
            <input type="text" name="title" placeholder="Enter a new task..." required>
            <select name="priority">
                <option value="1">P1 🔴 Urgent</option>
                <option value="2" selected>P2 🟡 High</option>
                <option value="3">P3 🟢 Normal</option>
                <option value="4">P4 🔵 Low</option>
            </select>
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


def render_edit_page(pos, task):
    """Render an inline edit form for a specific task."""
    pri = task["priority"]
    options = "".join(
        f'<option value="{p}" {"selected" if p == pri else ""}>P{p} {PRIORITY_LABEL[p]}</option>'
        for p in (1, 2, 3, 4)
    )
    edit_form = f"""\
<div class="container" style="margin-top:1rem">
    <h2 style="text-align:center;color:#1a1a2e;margin-bottom:1rem">✎ Edit Task #{pos}</h2>
    <form method="POST" action="/edit/{pos}" class="edit-form" style="justify-content:center">
        <input type="text" name="title" value="{task['title']}" required>
        <select name="priority">{options}</select>
        <button type="submit" class="btn btn-save">💾 Save</button>
        <a href="/" class="btn btn-cancel">Cancel</a>
    </form>
</div>"""
    return HTML_TEMPLATE.format(message_html="", tasks_html=edit_form)


def render_page(message="", msg_type="success"):
    """Render the todo list as an HTML page."""
    if todo_app.todos:
        items = []
        for i, t in enumerate(todo_app.todos, start=1):
            pri = t["priority"]
            pri_label = PRIORITY_LABEL.get(pri, "")
            pri_color = PRIORITY_COLOR.get(pri, "#4361ee")
            title_text = t["title"]
            done_class = "done" if t["done"] else ""
            title_class = "title" + (" done-text" if t["done"] else "")
            check_char = "✓" if t["done"] else "○"
            toggle_url = url_for('toggle', pos=i)
            delete_url = url_for('delete', pos=i)
            edit_url = url_for('edit', pos=i)

            items.append(
                f'<li class="task-item {done_class}" style="border-left-color:{pri_color}">'
                f'  <div class="left">'
                f'    <span class="num">{i}.</span>'
                f'    <span class="pri-tag" style="background:{pri_color}">P{pri} {pri_label}</span>'
                f'    <span class="{title_class}">{title_text}</span>'
                f'  </div>'
                f'  <div class="actions">'
                f'    <a href="{toggle_url}" class="btn btn-toggle">{check_char}</a>'
                f'    <a href="{edit_url}" class="btn btn-edit">✎</a>'
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


@app.route('/', methods=['GET'])
def index():
    return render_page()


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if not title:
        return render_page("Error: Task title cannot be empty.", "error")
    todo_app.add_one_task(title)
    return redirect(url_for('index'))


@app.route('/delete/<int:pos>', methods=['GET'])
def delete(pos):
    if not todo_app.todos:
        return render_page("Error: There are no tasks to delete.", "error")
    if pos < 1 or pos > len(todo_app.todos):
        return render_page(f"Error: Position {pos} is out of range.", "error")
    todo_app.delete_task(pos)
    return redirect(url_for('index'))


@app.route('/toggle/<int:pos>', methods=['GET'])
def toggle(pos):
    if not todo_app.todos:
        return render_page("Error: There are no tasks.", "error")
    if pos < 1 or pos > len(todo_app.todos):
        return render_page(f"Error: Position {pos} is out of range.", "error")
    todo_app.toggle_task(pos)
    return redirect(url_for('index'))


@app.route('/edit/<int:pos>', methods=['GET'])
def edit(pos):
    if not todo_app.todos:
        return render_page("Error: There are no tasks.", "error")
    if pos < 1 or pos > len(todo_app.todos):
        return render_page(f"Error: Position {pos} is out of range.", "error")
    t = todo_app.todos[pos - 1]
    return render_edit_page(pos, t)


@app.route('/edit/<int:pos>', methods=['POST'])
def edit_post(pos):
    if not todo_app.todos:
        return render_page("Error: There are no tasks.", "error")
    if pos < 1 or pos > len(todo_app.todos):
        return render_page(f"Error: Position {pos} is out of range.", "error")
    new_title = request.form.get('title', '').strip()
    if not new_title:
        return render_page("Error: Title cannot be empty.", "error")
    pri_str = request.form.get('priority', '').strip()
    new_pri = int(pri_str) if pri_str.isdigit() else None
    todo_app.edit_task(pos, new_title, new_pri)
    return redirect(url_for('index'))


@app.route('/save', methods=['GET'])
def save():
    todo_app.save_todos()
    return redirect(url_for('index'))


@app.route('/load', methods=['GET'])
def load():
    todo_app.load_todos()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
