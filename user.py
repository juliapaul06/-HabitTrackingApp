from storage import Storage
from habit import Habit
from datetime import datetime

class User:
    """
    Represents the user and manages their habits and tasks.
    """

    def __init__(self, name: str):
        self.name = name
        self.storage = Storage()
        self.habits = {habit.id: habit for habit in self.storage.load_habits()}
        self.next_id = max(self.habits.keys(), default=0) + 1

    def create_habit(self, name, periodicity):
        """
        Creates and saves a new habit.
        """
        habit = Habit(self.next_id, name, periodicity)
        self.habits[self.next_id] = habit
        self.storage.save_habit(habit)
        self.next_id += 1

    def edit_habit(self, habit_id, new_name, new_periodicity):
        """
        Edits an existing habit's name and periodicity. Resets tasks.
        """
        if habit_id in self.habits:
            habit = self.habits[habit_id]
            habit.name = new_name
            habit.periodicity = new_periodicity
            habit.reset_tasks()
            self.storage.update_habit(habit)
            self.storage.delete_tasks(habit_id)
        else:
            raise ValueError("Habit ID not found.")

    def delete_habit(self, habit_id):
        """
        Deletes a habit.
        """
        if habit_id in self.habits:
            del self.habits[habit_id]
            self.storage.delete_habit(habit_id)

    def list_habits(self):
        """
        Returns all habits.
        """
        return list(self.habits.values())

    def list_habits_by_periodicity(self, periodicity):
        """
        Filters habits based on their periodicity.
        """
        return [habit for habit in self.habits.values() if habit.periodicity == periodicity]

    def complete_task(self, habit_id, date):
        """
        Completes a task for a specific habit and date.
        """
        if habit_id in self.habits:
            habit = self.habits[habit_id]
            habit.complete_task(date)
            task = next(t for t in habit.tasks if t.date.date() == date.date())
            self.storage.save_task(habit_id, task)
        else:
            raise ValueError("Habit ID not found.")
