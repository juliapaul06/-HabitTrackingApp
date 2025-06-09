import sqlite3
from datetime import datetime
from habit import Habit, Task

class Storage:
    """
    Handles all database operations using SQLite for habits and their tasks.
    """

    def __init__(self):
        """
        Initializes the database connection and sets up the tables.
        """
        self.conn = sqlite3.connect("habits.db")
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        """
        Creates the 'habits' and 'tasks' tables in the database if they don't exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY,
                name TEXT,
                periodicity TEXT,
                created_at TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                habit_id INTEGER,
                date TEXT,
                is_complete INTEGER,
                completed_at TEXT,
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        ''')
        self.conn.commit()

    def save_habit(self, habit: Habit):
        """
        Saves a new habit into the database.
        """
        self.cursor.execute(
            'INSERT INTO habits (id, name, periodicity, created_at) VALUES (?, ?, ?, ?)',
            (habit.id, habit.name, habit.periodicity, habit.created_at.isoformat())
        )
        self.conn.commit()

    def update_habit(self, habit: Habit):
        """
        Updates the name and periodicity of an existing habit.
        """
        self.cursor.execute(
            'UPDATE habits SET name = ?, periodicity = ? WHERE id = ?',
            (habit.name, habit.periodicity, habit.id)
        )
        self.conn.commit()

    def get_habit_by_id(self, habit_id):
        """
        Retrieves a habit by its ID.
        """
        self.cursor.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
        row = self.cursor.fetchone()
        if row:
            habit = Habit(row[0], row[1], row[2], datetime.fromisoformat(row[3]))
            habit.tasks = self.load_tasks(habit.id)
            return habit
        return None

    def load_habits(self):
        """
        Loads all habits from the database.
        """
        self.cursor.execute('SELECT * FROM habits')
        rows = self.cursor.fetchall()
        habits = []
        for row in rows:
            habit = Habit(row[0], row[1], row[2], datetime.fromisoformat(row[3]))
            habit.tasks = self.load_tasks(habit.id)
            habits.append(habit)
        return habits

    def delete_habit(self, habit_id):
        """
        Deletes a habit and all its tasks.
        """
        self.cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        self.cursor.execute('DELETE FROM tasks WHERE habit_id = ?', (habit_id,))
        self.conn.commit()

    def delete_tasks(self, habit_id):
        """
        Deletes all tasks for a specific habit.
        """
        self.cursor.execute('DELETE FROM tasks WHERE habit_id = ?', (habit_id,))
        self.conn.commit()

    def save_task(self, habit_id, task: Task):
        """
        Saves a completed task into the database.
        """
        self.cursor.execute(
            'INSERT INTO tasks (habit_id, date, is_complete, completed_at) VALUES (?, ?, ?, ?)',
            (habit_id, task.date.isoformat(), int(task.is_complete), task.completed_at.isoformat())
        )
        self.conn.commit()

    def load_tasks(self, habit_id):
        """
        Loads all tasks for a specific habit.
        """
        self.cursor.execute('SELECT * FROM tasks WHERE habit_id = ?', (habit_id,))
        rows = self.cursor.fetchall()
        return [
            Task(datetime.fromisoformat(row[2]), bool(row[3]), datetime.fromisoformat(row[4]) if row[4] else None)
            for row in rows
        ]
