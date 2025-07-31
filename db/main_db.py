import sqlite3
from db import queries
from config import db_path


def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_task)
    print('База данных подключена!')
    conn.commit()
    conn.close()

def get_tasks(filter_type="all"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if filter_type == 'completed':
        cursor.execute(queries.SELECT_TASKS_completed)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.SELECT_TASKS_uncompleted)
    elif filter_type == 'in_work':
        cursor.execute(queries.SELECT_TASKS_in_work)
    else:
        cursor.execute(queries.SELECT_TASKS)

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(task):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def update_task(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if new_task is not None:
        cursor.execute(queries.UPDATE_TASK, (new_task, task_id))

    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))

    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()

def clear_completed():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE completed = 1")
    conn.commit()
    conn.close()

def clear_all():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()