from db import all_habits, daily_habits, weekly_habits, get_weekly_names_streaks, get_daily_names_streaks, get_daily_highscore, get_weekly_highscore, get_highscore, currstreak, get_start_date

def count_habits(db):
    data = all_habits(db)
    return len(data)

def count_daily_habits(db):
    data = daily_habits(db)
    return len(data)

def count_weekly_habits(db):
    data = weekly_habits(db)
    return len(data)

  
def daily_habits_streaks(db):
    habits = get_daily_names_streaks(db)
    if not habits:
        print("No daily habits found.")
        return
    
    for habit in habits:
        name, streak = habit
        print(f"Habit: {name} | Current Streak: {streak}")


def weekly_habits_streaks(db):
    habits = get_weekly_names_streaks(db)
    if not habits:
        print("No weekly habits found.")
        return
    
    for habit in habits:
        name, streak = habit
        print(f"Habit: {name} | Current Streak: {streak}")        

def best_daily_highscore(db):
    result = get_daily_highscore(db)
    if result:
        habit_name, highscore = result
        print(f"Your highscore for daily tasks is: {habit_name}, {highscore}")
    else:
        print("No highscore found for daily tasks")

def best_weekly_highscore(db):
    result = get_weekly_highscore(db)
    if result:
        habit_name, highscore = result
        print(f"Your highscore for weekly tasks is: {habit_name}, {highscore}")
    else:
        print("No highscore found for weekly tasks")        
      
def specific_highscore(db, habitName):
    highscore = get_highscore(db, habitName)
    print(f"Your highscore for {habitName} is: {highscore[0]}") 

def current_streak(db, habitName):
    streak = currstreak(db, habitName)
    print(f"Current streak for {habitName} is: {streak[0]}")    

def print_start(db, name):
    start = get_start_date(db, name)
    print(f"Started habit {name} on: {start[0]}")