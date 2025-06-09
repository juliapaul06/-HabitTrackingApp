Habit Tracker CLI

A lightweight command-line interface (CLI) habit tracker written in Python. Create, manage, and track your habits daily, weekly, or monthly with automatic streak tracking.

**Features**

- Add, edit, and delete habits.

- Mark tasks as completed.

- Automatically tracks current and max streaks.

- Supports periodicities: *daily*, *weekly*, and *monthly*.

- Calculates streaks based on actual date gaps (not just task count).

- Simple local file storage (JSON-based by default).

- Clear and friendly CLI interface.


**Setup Instructions**

Prerequisites

- Python 3.10+ installed

- IDE/Text Editor (e.g., *PyCharm*, *Visual Studio Code*)

- Git (optional, for cloning)


**Installing Python**

Download from: [https://www.python.org/downloads/]

Ensure you *check the box to add Python to PATH* during installation.

To check it's installed:

python --version

\# or sometimes

python3 –version


**Running the CLI App**

*Clone or Download*

You can either:

Copy

[*https://github.com/juliapaul06/-HabitTrackingApp.git*]

Or just download the ZIP and extract it.


**Project Structure**

habit-tracker/

├── main.py               # Entry point for CLI

├── habit.py              # Habit and Task classes

├── user.py               # User interaction logic

├── storage.py            # File-based storage system

├── analytics.py          # Streak calculation logic

├── test\_user.py          # Tests for creation/editing/deletion

├── test\_analytics.py     # Tests for streak logic

└── requirements.txt      # (optional) For external dependencies (none currently)


**Running the App**

In terminal:

Copy

python main.py

or (if Python 3):

python3 main.py

You’ll see a menu-driven interface:

Habit Tracker Menu

1. Create Habit

2. Edit Habit

3. Delete Habit

4. Complete Task

5. List Habits

6. Get Current Longest Streak

7. List Habits by Periodicity

8. Exit


**How Streaks Are Calculated**

🗓️ Daily

- Each task must be **exactly 1 day after** the last completed task to count toward a streak.
- Missing a day **breaks the streak**.

📅 Weekly (Strict Logic)

- Each task must be at least 7 days apart from the last task in the streak.
- Completing early or late *does not count* toward the next streak slot.


**Example Analysis:**

Habit: "Jog" (Weekly)\
Tasks:

2025-07-01 ✅ <-- First task

2025-07-08 ✅ <-- Exactly 7 days later → +1 streak

2025-07-09 ✅ <-- Only 1 day later → does NOT increase streak

2025-07-15 ✅ <-- 7 days after 07-08 → counts as new valid week → +1 streak

2025-07-23 ✅ <-- 8 days after 07-15 → too far for next week → current streak breaks

- So, your *max streak = 3* (01 → 08 → 15)
- The latest task (23rd) is *not* exactly a 7-day gap from 15th — hence *current streak resets = 1*

🗓️ Monthly

- Similar to weekly, but based on a strict 30-day period.


**Running Unit Tests**

To run the test suite:

Copy

python -m unittest test_user.py

python -m unittest test_analytics.py

These tests cover:

- Creating/editing/deleting habits
- Completing tasks
- Validating streak logic (including weekly & monthly)


**Notes**

- All data is saved locally in JSON files (via storage.py).
- Editing a habit resets progress (all tasks and streaks) to ensure clean tracking.
- You can extend this project with GUI, notifications, or database support.


**Author**

Made with ♥️ by Paul — a student passionate about clean Python design and helping others stay productive.


**LICENSE (MIT License)**

MIT License

Copyright (c) 2025 Paul

Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    

copies of the Software, and to permit persons to whom the Software is        

furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in   

all copies or substantial portions of the Software.                          

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    

FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     

FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         

DEALINGS IN THE SOFTWARE.

