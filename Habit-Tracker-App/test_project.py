from habit import Habit, dbHabit
from db import get_db, add_habit, check_off, all_habits, daily_habits, get_daily_names_streaks, get_highest_daily_streak
from analyse import count_habits


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")

        add_habit(self.db, "test_habit", "Daily")
        add_habit(self.db, "test_habit1", "Daily")
        add_habit(self.db, "test_habit2", "Daily")

        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit")
        check_off(self.db, "test_habit")


    def test_habit(self):
        habit = Habit("test_habit_1", "test_frequency_1")

        habit.check()
        habit.reset()
        habit.check()

    def test_dbhabit(self):
        dbhabit = dbHabit("test_dbHabit_2", "test_frequency_2") 

        dbhabit.check(self.db)   
        dbhabit.review(self.db) 
        dbhabit.review_all_habits(self.db)   

    def test_db(self):
        data = all_habits(self.db)
        assert len(data) == 3

        count = count_habits(self.db)
        assert count == 3

        highest_streak = get_highest_daily_streak(self.db)
        assert highest_streak[0] == 5  

    def teardown_method(self):
        import os
        os.remove("test.db")