from habit import Habit, dbHabit
from db import get_db, add_habit, check_off, all_habits, daily_habits, get_daily_names_streaks, get_highest_daily_streak
from analyse import count_habits

from datetime import date

class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")

        add_habit(self.db, "test_habit", "Daily")
        add_habit(self.db, "test_habit1", "Daily")
        add_habit(self.db, "test_habit2", "Daily")
        add_habit(self.db, "test_habit3", "Daily")
        add_habit(self.db, "test_habit4", "Weekly")
        add_habit(self.db, "test_habit5", "Weekly")

        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit3")
        check_off(self.db, "test_habit3")
        check_off(self.db, "test_habit3")


    def test_habit(self):
        habit = Habit("test_habit_1", "test_frequency_1")

        habit.check()
        habit.reset()
        habit.check()

    def test_dbhabit(self):
        dbhabit = dbHabit("test_habit3", "Daily", last_checked = "Not Checked")         

        dbhabit.check(self.db) 
        print(dbhabit.last_checked)
        print(date.today().strftime("%Y-%m-%d"))
        assert dbhabit.streak == 1
        assert str(dbhabit.last_checked) == date.today().strftime("%Y-%m-%d")

        ###Test if streak gets reset when not checked off for a day###
        dbhabit1 = dbHabit("test_habit3", "Daily", streak = 4, last_checked = "2023-07-13")   

        dbhabit1.review(self.db) 
        assert dbhabit1.streak == 0

        dbhabit1.check_highscore(self.db)
        assert dbhabit1.highscore == 3

        dbhabit.review_all_habits(self.db)   

    def test_db(self):
        data = all_habits(self.db)
        assert len(data) == 6

        count = count_habits(self.db)
        assert count == 6

        highest_streak = get_highest_daily_streak(self.db)
        assert highest_streak[0] == 5  

    def teardown_method(self):
        import os
        os.remove("test.db")