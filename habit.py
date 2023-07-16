
from db import add_habit, check_off, get_highscore, new_highscore, currstreak, reset_streak, all_habits, get_habit_last_checked
from datetime import datetime, date, timedelta


today = date.today()

"""
Represents a habit class with its properties and methods

Attributes:
        name (str): The name of the habit.
        frequency (str): The frequency of the habit (e.g., "Daily", "Weekly").
        streak (int): The current streak count for the habit.
        highscore (int): The highest streak count achieved for the habit.
        start (datetime.date): The start date of the habit.
        last_checked (datetime.date): The last checked date of the habit. string Not Checked if not checked yet.
"""
class Habit:

    def __init__(self, name, frequency, streak = 0, highscore = 0, start = date.today(), last_checked = "Not Checked"):
        self.name = name
        self.frequency = frequency
        self.streak = streak
        self.highscore = highscore
        self.start = start
        self.last_checked = last_checked

    def check(self):
        """Increases the streak count and updates the last checked date."""
        self.streak += 1
        self.last_checked = today

    def reset(self):
        """Resets the streak count to zero."""
        self.streak = 0

"""
    Represents a habit with additional functionality for database integration.

    Inherits from:
        Habit
""" 
class dbHabit(Habit):  

    def __init__(self, name, frequency, streak = 0, highscore = 0, start = date.today(), last_checked = "Not Checked"):
        super().__init__(name, frequency, streak, highscore, start)
        self.last_checked = last_checked  

    def increment(self, db):
        """Increments the streak count, updates the last checked date, and stores the update in the database."""
        check_off(db, self.name)
        self.last_checked = today
        self.streak += 1

    def check_highscore(self, db):
        """Checks if the current streak is higher than the highscore and updates it in the database."""
        highscore = get_highscore(db, self.name)
        currentstreak = currstreak(db, self.name)    
        if currentstreak >= highscore:
            self.highscore = highscore
            new_highscore(db, self.name)
            

    def review(self, db):
        """Reviews the habit's streak and resets it if it was not checked off in the respective frequency."""

        if self.frequency == "Daily":
            if self.last_checked == "Not Checked":
                return   
            
            last_checked_date = datetime.strptime(str(self.last_checked), "%Y-%m-%d").date()
            one_day_ago = today - timedelta(days=1)
            if last_checked_date < one_day_ago:
                reset_streak(db, self.name)
                self.reset()

        if self.frequency == "Weekly":
            if self.last_checked == "Not Checked":
                return
            
            last_checked_date = datetime.strptime(str(self.last_checked), "%Y-%m-%d").date()
            one_week_ago = today - timedelta(weeks=1)
            if last_checked_date < one_week_ago:
                reset_streak(db, self.name)  
                self.reset()
   
       
    @staticmethod                                    
    def review_all_habits(db):
        """Reviews all habits in the database and updates their streaks accordingly."""
        habits = get_habit_last_checked(db)

        for habit in habits:
            name = habit[0]
            frequency = habit[1]
            last_checked = habit[2]

            habit_instance = dbHabit(name, frequency)
            habit_instance.last_checked = last_checked
            habit_instance.review(db)


    def check(self, db):
        """Checks off the habit for the current day if habit has not been checked off in specific frequency """
        if self.frequency == "Daily":
            if self.last_checked != "Not Checked":
                last_checked_date = datetime.strptime(str(self.last_checked), "%Y-%m-%d").date()
                if last_checked_date == today:
                    print("You have already checked off this habit today.")
                    return
                elif last_checked_date != today:
                    self.increment(db)
                    self.check_highscore(db)
                    print(f"habit {self.name} checked off for today")
                 
            else:
                self.increment(db)
                self.check_highscore(db)
                print(f"habit {self.name} checked off for today")   

        elif self.frequency == "Weekly":
            if self.last_checked == "Not Checked":
                self.increment(db)
                self.check_highscore(db)    
                print(f"habit {self.name} checked off for this week")

            else:
                last_checked_date = datetime.strptime(str(self.last_checked), "%Y-%m-%d").date()
                last_checked_week_start = last_checked_date - timedelta(days=last_checked_date.weekday())
                if last_checked_week_start != today - timedelta(days=today.weekday()):
                    self.increment(db)   
                    self.check_highscore(db) 
                    print(f"habit {self.name} checked off for this week")

                else:
                    print("You have already checked off this habit this week.") 
                                           

    def store(self, db):
        """stores new habit in the database"""
        add_habit(db, self.name, self.frequency, self.last_checked)    
     