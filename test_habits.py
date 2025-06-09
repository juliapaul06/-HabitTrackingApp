import unittest
from datetime import datetime, timedelta
from habit import Habit
from user import User

class MockStorage:
    """Mock storage class to simulate saving and retrieving habits and tasks, avoiding real file/database interactions."""
    def __init__(self):
        self.habits = {}
        self.tasks = {}

    def load_habits(self):
        return list(self.habits.values())

    def save_habit(self, habit):
        self.habits[habit.id] = habit

    def update_habit(self, habit):
        self.habits[habit.id] = habit

    def delete_habit(self, habit_id):
        if habit_id in self.habits:
            del self.habits[habit_id]

    def save_task(self, habit_id, task):
        self.tasks.setdefault(habit_id, []).append(task)

    def delete_tasks(self, habit_id):
        if habit_id in self.tasks:
            del self.tasks[habit_id]


class TestUserHabitOperations(unittest.TestCase):
    """Unit tests to validate creation, editing, deletion, and task completion of habits by a User."""

    def setUp(self):
        # Setup a User with mock storage before each test
        self.user = User("TestUser")
        self.user.storage = MockStorage()  # Replace real storage with mock
        self.user.habits = {}
        self.user.next_id = 1  # Start ID from 1 for predictability

    def test_create_habit(self):
        """Test if a habit can be created and stored properly."""
        self.user.create_habit("Read Book", "daily")
        self.assertEqual(len(self.user.habits), 1)
        habit = list(self.user.habits.values())[0]
        self.assertEqual(habit.name, "Read Book")
        self.assertEqual(habit.periodicity, "daily")
        self.assertEqual(habit.id, 1)

    def test_edit_habit_name_and_periodicity(self):
        """Test editing a habit's name and periodicity, and ensure tasks are reset."""
        self.user.create_habit("Exercise", "weekly")
        habit_id = 1
        self.user.edit_habit(habit_id, "Jogging", "daily")
        habit = self.user.habits[habit_id]
        self.assertEqual(habit.name, "Jogging")
        self.assertEqual(habit.periodicity, "daily")
        self.assertEqual(len(habit.tasks), 0)  # Task list should be cleared after edit

    def test_delete_habit(self):
        """Test deleting a habit by ID and ensure it's removed from user's habit list."""
        self.user.create_habit("Meditate", "daily")
        habit_id = 1
        self.user.delete_habit(habit_id)
        self.assertNotIn(habit_id, self.user.habits)

        # Deleting a non-existent habit should not raise an error
        self.user.delete_habit(99)  # Should silently pass without crashing

    def test_complete_task_creates_and_saves_task(self):
        """Test if completing a task correctly adds it to the habit and saves to storage."""
        self.user.create_habit("Yoga", "daily")
        habit_id = 1
        date = datetime(2025, 6, 9)
        self.user.complete_task(habit_id, date)

        habit = self.user.habits[habit_id]
        # Confirm task was added to habit
        self.assertEqual(len(habit.tasks), 1)
        self.assertEqual(habit.tasks[0].date.date(), date.date())
        self.assertTrue(habit.tasks[0].is_complete)

        # Confirm task was saved in storage
        self.assertIn(habit_id, self.user.storage.tasks)
        saved_tasks = self.user.storage.tasks[habit_id]
        self.assertEqual(saved_tasks[0].date.date(), date.date())

    def test_complete_task_invalid_habit(self):
        """Test completing a task for a non-existent habit should raise an error."""
        with self.assertRaises(ValueError):
            self.user.complete_task(999, datetime.now())

    def test_edit_habit_invalid_id_raises(self):
        """Test editing a habit with a non-existent ID should raise an error."""
        with self.assertRaises(ValueError):
            self.user.edit_habit(999, "NewName", "monthly")


if __name__ == "__main__":
    unittest.main()
