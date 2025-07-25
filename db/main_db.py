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

def add_task(task):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def update_task(task_id, new_task):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_TASK, (new_task, task_id))
    conn.commit()
    conn.close()

def deelete_task(task_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()