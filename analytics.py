from functools import reduce

class Analytics:
    @staticmethod
    def update_streak(tasks, periodicity: str) -> (int, int):
        """Functional approach to calculate current and max streaks."""

        # Sort tasks by date
        sorted_tasks = sorted(tasks, key=lambda t: t.date)

        def streak_calculator(acc, task):
            last_date, current_streak, max_streak = acc

            if task.is_complete:
                if last_date is None:
                    # First completed task
                    return (task.date, 1, 1)

                delta_days = (task.date.date() - last_date.date()).days

                if periodicity == 'Daily':
                    if delta_days == 1:
                        new_streak = current_streak + 1
                    elif delta_days > 1:
                        new_streak = 1
                    else:
                        return acc  # same day or earlier — skip
                    return (task.date, new_streak, max(new_streak, max_streak))

                elif periodicity == 'Weekly':
                    if delta_days == 7:
                        new_streak = current_streak + 1
                    elif delta_days > 7:
                        new_streak = 1
                    else:
                        return acc  # too soon or duplicate — skip
                    return (task.date, new_streak, max(new_streak, max_streak))

                elif periodicity == 'Monthly':
                    # If same month and year, it's a duplicate — skip it
                    if task.date.year == last_date.year and task.date.month == last_date.month:
                        return acc

                    # Treat monthly streak as strict ~1-month gap (28-31 days)
                    if 28 <= delta_days <= 31:
                        new_streak = current_streak + 1
                    elif delta_days > 31:
                        new_streak = 1  # too late — missed the cycle
                    else:
                        return acc  # early duplicate or same month — skip

                    return (task.date, new_streak, max(new_streak, max_streak))

            return acc  # task is not completed — skip

        # Run the functional reducer
        _, current_streak, max_streak = reduce(streak_calculator, sorted_tasks, (None, 0, 0))
        return current_streak, max_streak

    @staticmethod
    def get_longest_streak(habits) -> (str, int):
        """Return the habit with the longest streak."""
        streaks = map(
            lambda habit: (habit.name, Analytics.update_streak(habit.get_tasks(), habit.periodicity)[1]),
            habits
        )
        return max(streaks, key=lambda x: x[1], default=(None, 0))

    @staticmethod
    def get_longest_streak_for_habit(habit) -> int:
        """Return the longest streak for a specific habit."""
        return Analytics.update_streak(habit.get_tasks(), habit.periodicity)[1]
