from datetime import datetime
from typing import List

class Task:
    """
    Represents a single task (instance of a habit) on a specific date.
    """

    def __init__(self, date: datetime, is_complete=False, completed_at=None):
        self.date = date
        self.is_complete = is_complete
        self.completed_at = completed_at

    def complete(self, completed_at: datetime):
        """
        Marks the task as complete and stores the completion timestamp.
        """
        self.is_complete = True
        self.completed_at = completed_at

class Habit:
    """
    Represents a habit with periodicity and a list of tasks.
    """

    def __init__(self, habit_id: int, name: str, periodicity: str, created_at=None):
        self.id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()
        self.tasks: List[Task] = []

    def get_tasks(self):
        """
        Returns all tasks associated with the habit.
        """
        return self.tasks

    def complete_task(self, date: datetime):
        """
        Marks a task as complete on a specific date or adds a new completed task.
        """
        task = next((t for t in self.tasks if t.date.date() == date.date()), None)
        if task:
            task.complete(datetime.now())
        else:
            new_task = Task(date)
            new_task.complete(datetime.now())
            self.tasks.append(new_task)

    def reset_tasks(self):
        """
        Clears all tasks (used when editing a habit).
        """
        self.tasks = []
