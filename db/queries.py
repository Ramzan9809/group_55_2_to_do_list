CREATE_TABLE_task = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_done INTEGER DEFAULT 0
);
"""





INSERT_TASK = "INSERT INTO tasks (task, created_at) VALUES (?, ?)"
SELECT_TASKS = "SELECT id, task, created_at, is_done FROM tasks"


UPDATE_TASK = "UPDATE tasks SET task = ? WHERE id = ?"

DELETE_TASK = "DELETE FROM tasks WHERE id = ?"