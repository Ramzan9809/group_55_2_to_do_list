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

def get_tasks():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.SELECT_TASKS)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(task, created_at):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (task, created_at, is_done) VALUES (?, ?, 0)",
            (task, created_at)
        )
        conn.commit()
        return cursor.lastrowid



def update_task(task_id, new_task):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_TASK, (new_task, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()

def update_status(task_id, is_done):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET is_done = ? WHERE id = ?",
            (is_done, task_id)
        )
        conn.commit()