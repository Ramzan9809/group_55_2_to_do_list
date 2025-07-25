CREATE_TABLE_task = """
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    task TEXT NOT NULL
    )
"""

INSERT_TASK = """
    INSERT INTO tasks (task) VALEUS (?)
"""

SELECT_TASKS = "SELECT id, task FROM tasks"

UPDATE_TASK = "UPDATE tasks SET task = ? WHERE id = ?"

DELETE_TASK = "DELETE FROM tasks WHERE id = ?"