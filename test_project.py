from habit import Habit, dbHabit
from db import get_db, add_habit, check_off, all_habits, get_start_date, get_highest_daily_streak
from analyse import count_habits

from datetime import date, datetime

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
        assert habit.streak == 1

        habit.reset()
        assert habit.streak == 0


    def test_dbhabit(self):
        dbhabit = dbHabit("test_habit3", "Daily", last_checked = "Not Checked")         

        dbhabit.check(self.db) 
        print(dbhabit.last_checked)
        print(date.today().strftime("%Y-%m-%d"))
        assert dbhabit.streak == 1
        assert str(dbhabit.last_checked) == date.today().strftime("%Y-%m-%d")

        dbhabit.check(self.db)
        assert dbhabit.streak == 1


        dbhabit1 = dbHabit("test_habit4", "Weekly")

        dbhabit1.last_checked = "2023-06-12"
        dbhabit1.check(self.db)

        dbhabit1.last_checked = "2023-06-19"
        dbhabit1.check(self.db)

        #test if check_highscore stays correct after streak gets reset
        dbhabit1.last_checked = "2023-06-26"
        dbhabit1.check_highscore(self.db)
        assert dbhabit1.highscore == 2

        #test if review resets streak to 0 since a week has been missed to check off
        dbhabit1.review(self.db)
        assert dbhabit1.streak == 0

        dbHabit.review_all_habits(self.db)   

    def test_db(self):
        data = all_habits(self.db)
        assert len(data) == 6

        #Test if the number of habits in the database gets retrieved correctly.
        count = count_habits(self.db)
        assert count == 6

        #Test if the highest daily streak in the database gets retrieved correctly.
        highest_streak = get_highest_daily_streak(self.db)
        assert highest_streak[0] == 5  
        
        #Test if the start date for the habit matches today's date.
        start_date = get_start_date(self.db, "test_habit3")
        assert datetime.strptime(start_date[0], "%Y-%m-%d").date() == date.today()


    def teardown_method(self):
        import os
        os.remove("test.db")