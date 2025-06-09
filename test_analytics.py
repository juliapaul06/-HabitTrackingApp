import unittest
from datetime import datetime, timedelta
from habit import Habit, Task
from analytics import Analytics

class TestAnalytics(unittest.TestCase):
    """
    Unit tests for the Analytics class, which handles streak calculations.
    Covers Daily, Weekly, and Monthly streak logic using sample habits and tasks.
    """

    def create_tasks(self, dates, completed=True):
        """
        Helper method to create a list of completed Task objects for given dates.
        Useful for simulating task completion across time intervals.
        """
        tasks = []
        for d in dates:
            task = Task(d)
            if completed:
                task.is_complete = True
            tasks.append(task)
        return tasks

    def test_daily_streak_perfect(self):
        """
        Test perfect daily streak: 5 tasks on consecutive days.
        Expected: current and max streak both = 5.
        """
        base_date = datetime(2025, 6, 1)
        dates = [base_date + timedelta(days=i) for i in range(5)]
        tasks = self.create_tasks(dates)
        current_streak, max_streak = Analytics.update_streak(tasks, "Daily")
        self.assertEqual(current_streak, 5)
        self.assertEqual(max_streak, 5)

    def test_daily_streak_with_gap(self):
        """
        Test daily streak with a 1-day gap.
        Expected: current = 1 (last task), max = 2 (first two tasks).
        """
        base_date = datetime(2025, 6, 1)
        dates = [base_date, base_date + timedelta(days=1), base_date + timedelta(days=3)]
        tasks = self.create_tasks(dates)
        current_streak, max_streak = Analytics.update_streak(tasks, "Daily")
        self.assertEqual(current_streak, 1)
        self.assertEqual(max_streak, 2)

    def test_weekly_streak_perfect(self):
        """
        Test perfect weekly streak: tasks done exactly every 7 days.
        Expected: current and max streak both = 3.
        """
        base_date = datetime(2025, 6, 1)  # Sunday
        dates = [base_date + timedelta(days=7*i) for i in range(3)]
        tasks = self.create_tasks(dates)
        current_streak, max_streak = Analytics.update_streak(tasks, "Weekly")
        self.assertEqual(current_streak, 3)
        self.assertEqual(max_streak, 3)

    def test_weekly_streak_with_skips(self):
        """
        Test weekly streak with a skip (8-day gap), then a valid 7-day one.
        Expected: current = 2 (from 6/9 to 6/16), max = 2.
        """
        base_date = datetime(2025, 6, 1)
        dates = [base_date, base_date + timedelta(days=8), base_date + timedelta(days=15)]
        tasks = self.create_tasks(dates)
        current_streak, max_streak = Analytics.update_streak(tasks, "Weekly")
        self.assertEqual(current_streak, 2)
        self.assertEqual(max_streak, 2)

    def test_weekly_streak_partial(self):
        """
        Test weekly streak where one task breaks the cycle (14-day gap).
        Expected: current = 1 (last task only), max = 2 (first two).
        """
        base_date = datetime(2025, 6, 1)
        dates = [base_date, base_date + timedelta(days=7), base_date + timedelta(days=21)]
        tasks = self.create_tasks(dates)
        current_streak, max_streak = Analytics.update_streak(tasks, "Weekly")
        self.assertEqual(current_streak, 1)
        self.assertEqual(max_streak, 2)

    def test_monthly_streak_perfect(self):
        """
        Test monthly streak with tasks done on the 1st of 3 consecutive months.
        Expected: current and max streak both = 3.
        """
        dates = [datetime(2025, m, 1) for m in range(1, 4)]  # Jan, Feb, Mar
        tasks = self.create_tasks(dates)
        current_streak, max_streak = Analytics.update_streak(tasks, "Monthly")
        self.assertEqual(current_streak, 3)
        self.assertEqual(max_streak, 3)

    def test_monthly_streak_with_gap(self):
        """
        Test monthly streak with a gap (missing March).
        Expected: current = 1 (April), max = 2 (Jan & Feb).
        """
        dates = [datetime(2025, 1, 1), datetime(2025, 2, 1), datetime(2025, 4, 1)]
        tasks = self.create_tasks(dates)
        current_streak, max_streak = Analytics.update_streak(tasks, "Monthly")
        self.assertEqual(current_streak, 1)
        self.assertEqual(max_streak, 2)

    def test_get_longest_streak(self):
        """
        Test comparison across multiple habits to find which has the longest streak.
        Habit1 has 3-day streak, Habit2 has 2-week streak.
        Expected: Habit1 is longest with streak = 3.
        """
        # Habit 1: Daily streak of 3
        habit1 = Habit(1, "Habit1", "Daily")
        habit1.tasks = self.create_tasks([datetime(2025,6,1) + timedelta(days=i) for i in range(3)])
        
        # Habit 2: Weekly streak of 2
        habit2 = Habit(2, "Habit2", "Weekly")
        habit2.tasks = self.create_tasks([datetime(2025,6,1), datetime(2025,6,8)])
        
        longest = Analytics.get_longest_streak([habit1, habit2])
        self.assertEqual(longest, ("Habit1", 3))

# Run the tests when this file is executed
if __name__ == "__main__":
    unittest.main()
