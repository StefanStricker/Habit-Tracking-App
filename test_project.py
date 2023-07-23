from habit import Habit, dbHabit
from db import get_db, get_highscore, check_off, all_habits, get_start_date, get_highest_daily_streak, get_habit_data, currstreak
from analyse import count_habits

from datetime import date, datetime

class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")
        cursor = self.db.cursor()
        cursor.executemany(
            "INSERT INTO habits (name, frequency, last_checked, start) VALUES (?, ?, ?, ?)",
            [
                ("Test_Habit_1", "Daily", "2023-07-16", "2023-06-01"),
                ("Test_Habit_2", "Weekly", "2023-07-14", "2023-04-17"),
                ("Test_Habit_3", "Daily", "2023-07-12", "2023-06-06"),
                ("Test_Habit_4", "Daily", "2023-07-16", "2023-05-07"),
                ("Test_Habit_5", "Weekly", "2023-07-08", "2023-07-08"),
                ("Test_Habit_6", "Daily", "2023-07-16", "2023-03-22"),
                ("Test_Habit_7", "Weekly", "2023-07-01", "2023-06-12"),
            ]
        )
        self.db.commit()

        cursor.executemany(
            "INSERT INTO streak (currentstreak, highscore, habitName) VALUES (?, ?, ?)",
            [
                ("4", "13", "Test_Habit_1"),
                ("1", "2", "Test_Habit_2"),
                ("6", "6", "Test_Habit_3"),
                ("5", "12", "Test_Habit_4"),
                ("0", "1", "Test_Habit_5"),
                ("12", "12", "Test_Habit_6"),
                ("7", "7", "Test_Habit_7"),
            ]
        )
        self.db.commit()

    def test_habit_1(self):  
        #test if habit data gets retrieved corretly      
        habit1 = get_habit_data(self.db, "Test_Habit_1")
        streak = currstreak(self.db, "Test_Habit_1")
        highscore = get_highscore(self.db, "Test_Habit_1")
        assert streak == 4
        assert highscore == 13
        assert habit1[1] == "Daily"

    def test_habit(self):
        #test habit.check and habit.reset
        habit = Habit("test_habit_1", "test_frequency_1")

        habit.check()
        assert habit.streak == 1
        habit.reset()
        assert habit.streak == 0


    def test_dbhabit(self):
        #test if last_checked and streak get updated correctly
        dbhabit = dbHabit("Test_Habit_1", "Daily", last_checked = "Not Checked")         
        dbhabit.check(self.db) 
        print(dbhabit.last_checked)
        print(date.today().strftime("%Y-%m-%d"))
        assert dbhabit.streak == 1
        assert str(dbhabit.last_checked) == date.today().strftime("%Y-%m-%d")

        dbhabit.check(self.db)
        assert dbhabit.streak == 1


        dbhabit1 = dbHabit("Test_Habit_5", "Weekly")

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
        assert len(data) == 7

        #Test if the number of habits in the database gets retrieved correctly.
        count = count_habits(self.db)
        assert count == 7

        #Test if the highest daily streak in the database gets retrieved correctly.
        highest_streak = get_highest_daily_streak(self.db)
        assert highest_streak[0] == 12 
        
        #Test if the start date for the habit gets retrieved correcty.
        start_date = get_start_date(self.db, "Test_Habit_3")
        assert datetime.strptime(start_date[0], "%Y-%m-%d").date() ==  datetime(2023, 6, 6).date()


    def teardown_method(self):
        import os
        os.remove("test.db")