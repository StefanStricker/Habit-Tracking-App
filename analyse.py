from db import all_habits, daily_habits, weekly_habits, get_weekly_names_streaks, get_daily_names_streaks, get_daily_highscore, get_weekly_highscore, get_highscore, currstreak, get_start_date

def count_habits(db):
    """returns number of habits total"""
    data = all_habits(db)
    return len(data)

def count_daily_habits(db):
    """returns number of daily habits"""
    data = daily_habits(db)
    return len(data)

def count_weekly_habits(db):
    """returns number of weekly habits"""
    data = weekly_habits(db)
    return len(data)
 
def daily_habits_streaks(db):
    """prints all daily habits and the current streak""" 
    habits = get_daily_names_streaks(db)
    if not habits:
        print("No daily habits found.")
        return
    
    for habit in habits:
        name, streak = habit
        print(f"Habit: {name} | Current Streak: {streak}")
 
def weekly_habits_streaks(db):
    """prints all weekly habits and the current streak""" 
    habits = get_weekly_names_streaks(db)
    if not habits:
        print("No weekly habits found.")
        return
    
    for habit in habits:
        name, streak = habit
        print(f"Habit: {name} | Current Streak: {streak}")        
 
def best_daily_highscore(db):
    """prints highscore for daily habits""" 
    result = get_daily_highscore(db)
    if result:
        habit_name, highscore = result
        print(f"Your highscore for daily tasks is: {habit_name}, {highscore}")
    else:
        print("No highscore found for daily tasks")

def best_weekly_highscore(db):
    """prints highscore for weekly habits""" 
    result = get_weekly_highscore(db)
    if result:
        habit_name, highscore = result
        print(f"Your highscore for weekly tasks is: {habit_name}, {highscore}")
    else:
        print("No highscore found for weekly tasks")        
     
def specific_highscore(db, habitName):
    """prints highscore for specific habit""" 
    highscore = get_highscore(db, habitName)
    print(f"Your highscore for {habitName} is: {highscore}") 

def current_streak(db, habitName):
    """prints current streak for specific habit"""
    streak = currstreak(db, habitName)
    print(f"Current streak for {habitName} is: {streak}")    

def print_start(db, name):
    """prints start date for specific habit"""
    start = get_start_date(db, name)
    print(f"Started habit {name} on: {start[0]}")
