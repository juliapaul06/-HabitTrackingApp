import sys
from datetime import datetime
from user import User
from analytics import Analytics

class CLI:
    """
    Command-line interface for interacting with the habit tracker.
    """

    def __init__(self):
        self.user = User("John Doe")

    def display_menu(self):
        """
        Displays the main menu options.
        """
        print("\nHabit Tracker Menu")
        print("1. Create Habit")
        print("2. Edit Habit")
        print("3. Delete Habit")
        print("4. Complete Task")
        print("5. List Habits")
        print("6. Get Current Longest Streak")
        print("7. List Habits by Periodicity")
        print("8. Exit")

    def get_input(self):
        return input("Select an option: ")

    def display_message(self, msg):
        print(msg)

    def display_habits(self, habits):
        """
        Nicely prints out the user's habits and their details.
        """
        if not habits:
            print("No habits found.")
            return
        for habit in habits:
            current_streak, max_streak = Analytics.update_streak(habit.get_tasks(), habit.periodicity)
            print(f"ID {habit.id}: {habit.name} - {habit.periodicity}, Created: {habit.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Current Streak: {current_streak}, Max Streak: {max_streak}")
            for task in habit.get_tasks():
                status = "Completed" if task.is_complete else "Pending"
                completed_at = task.completed_at.strftime('%Y-%m-%d %H:%M:%S') if task.completed_at else "N/A"
                print(f"    Task: {task.date.strftime('%Y-%m-%d')}, Status: {status}, Completed At: {completed_at}")

    def handle_user_selection(self, sel):
        """
        Handles user selection from the menu.
        """
        if sel == "1":
            name = input("Enter habit name: ")
            periodicity = {"1": "Daily", "2": "Weekly", "3": "Monthly"}.get(
                input("Select periodicity (1. Daily, 2. Weekly, 3. Monthly): "), "Daily")
            self.user.create_habit(name, periodicity)
            self.display_message("Habit created.")

        elif sel == "2":
            try:
                habit_id = int(input("Enter habit ID to edit: "))
                new_name = input("Enter new name for the habit: ")
                new_periodicity = {"1": "Daily", "2": "Weekly", "3": "Monthly"}.get(
                    input("Enter new periodicity (1. Daily, 2. Weekly, 3. Monthly): "), "Daily")
                self.user.edit_habit(habit_id, new_name, new_periodicity)
                self.display_message("Habit updated and progress reset.")
            except ValueError:
                self.display_message("Invalid input.")

        elif sel == "3":
            try:
                habit_id = int(input("Enter habit ID to delete: "))
                self.user.delete_habit(habit_id)
                self.display_message("Habit deleted.")
            except ValueError:
                self.display_message("Invalid habit ID.")

        elif sel == "4":
            try:
                habit_id = int(input("Enter habit ID to complete task for: "))
                date_str = input("Enter date (YYYY-MM-DD): ")
                date = datetime.strptime(date_str, "%Y-%m-%d")
                self.user.complete_task(habit_id, date)
                self.display_message("Task completed.")
            except ValueError:
                self.display_message("Invalid input.")

        elif sel == "5":
            habits = self.user.list_habits()
            self.display_habits(habits)

        elif sel == "6":
            habits = self.user.list_habits()
            if habits:
                name, longest = Analytics.get_longest_streak(habits)
                self.display_message(f"Longest streak: {longest} periods (Habit: {name})")
            else:
                self.display_message("No habits found.")

        elif sel == "7":
            periodicity = {"1": "Daily", "2": "Weekly", "3": "Monthly"}.get(
                input("Select periodicity (1. Daily, 2. Weekly, 3. Monthly): "), "Daily")
            filtered = self.user.list_habits_by_periodicity(periodicity)
            self.display_habits(filtered)

        elif sel == "8":
            self.display_message("Exiting...")
            sys.exit()

        else:
            self.display_message("Invalid selection.")

if __name__ == "__main__":
    cli = CLI()
    while True:
        cli.display_menu()
        option = cli.get_input()
        cli.handle_user_selection(option)
