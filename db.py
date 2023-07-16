import sqlite3
from datetime import date


def get_db(name="main.db"):
    """
    Establishes a connection to the SQLite database and creates the necessary tables if they don't exist.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Creates the Database Tables
    """
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
        name TEXT PRIMARY KEY, 
        frequency TEXT,
        last_checked TEXT DEFAULT NULL, 
        start TEXT)""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS streak (
        currentstreak INT DEFAULT 0,
        highscore INT DEFAULT 0,
        habitName TEXT,
        FOREIGN KEY (habitName) REFERENCES habits(name))""")    
    
    db.commit()   
     

def add_habit(db, name, frequency, last_checked="Not Checked"):
    """adds a habit to the db and creates streak related to the habit"""
    cur = db.cursor()
    cur.execute("INSERT OR IGNORE INTO habits VALUES (?, ?, ?, ?)", (name, frequency, last_checked, date.today()))
    db.commit()

    cur.execute("INSERT OR IGNORE INTO streak (currentstreak, habitName) VALUES (?, ?)",(0, name))
    db.commit()

def check_off(db, habitName):
    """checks off the habit and updates last checked value to today"""
    cur = db.cursor()
    cur.execute("UPDATE streak SET currentstreak =  currentstreak + 1 WHERE habitName = ?", (habitName,))
    cur.execute("UPDATE habits SET last_checked = ? WHERE name = ?", (date.today(), habitName))
    db.commit()

def all_habits(db):
    """Select every record from the habits table"""
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
    return cur.fetchall()

def daily_habits(db):
    """Selects all entries from daily habits"""
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE frequency = 'Daily'")
    return cur.fetchall()

def weekly_habits(db):
    """Selects all entries from daily habits"""
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE frequency = 'Weekly'")
    return cur.fetchall()

def get_daily_names_streaks(db):
    """Selects all habit names and related streak for daily habits"""
    cur = db.cursor()
    cur.execute("SELECT habits.name, streak.currentstreak FROM habits INNER JOIN streak ON habits.name = streak.habitName WHERE frequency = 'Daily'")
    return cur.fetchall()

def get_weekly_names_streaks(db):
    """Selects all habit names and related streak for weekly habits"""
    cur = db.cursor()
    cur.execute("SELECT habits.name, streak.currentstreak FROM habits INNER JOIN streak ON habits.name = streak.habitName WHERE frequency = 'Weekly'")
    return cur.fetchall()

def get_highest_daily_streak(db):
    """Selects the highest currentstreak from all daily habits"""
    cur = db.cursor()
    cur.execute("SELECT MAX(currentstreak) FROM streak INNER JOIN habits ON habitName = habits.name WHERE habits.frequency = 'Daily'")
    return cur.fetchone()

def get_highest_weekly_streak(db):
    """Selects the highest currentstreak from all weekly habits"""
    cur = db.cursor()
    cur.execute("SELECT MAX(currentstreak) FROM streak INNER JOIN habits ON habitName = habits.name WHERE habits.frequency = 'Weekly'")    
    return cur.fetchone()

def currstreak(db, habitName):
    """Selects the current streak for a specific habit"""
    cur = db.cursor()
    cur.execute("SELECT currentstreak FROM streak WHERE habitName = ?", (habitName,))
    result = cur.fetchone()
    if result:
        currentstreak = result[0]
    else:
        currentstreak = 0
    return currentstreak
    
def get_habit_data(db, name):
    """Selects all data entries for a specific habit from the habits table"""
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE name = ?", (name,))
    return cur.fetchone()    

def get_highscore(db, habitName):
    """Selects the highscore for a specific habit"""
    cur = db.cursor()
    cur.execute("SELECT highscore FROM streak WHERE habitName = ?", (habitName,))
    result = cur.fetchone()
    if result:
        highscore = result[0]
    else:
        highscore = 0
    return highscore   

def new_highscore(db, habitName):
    """Updates the highscore for a specific habit"""
    cur = db.cursor()
    cur.execute("UPDATE streak SET highscore = currentstreak WHERE habitName = ?", (habitName,))
    db.commit()

def get_daily_highscore(db):
    """Selects the biggest highscore Value from all daily habits"""
    cur = db.cursor()
    cur.execute("SELECT habits.name, MAX(highscore) FROM streak INNER JOIN habits ON streak.habitName = habits.name WHERE frequency = 'Daily'")
    return cur.fetchone() 

def get_weekly_highscore(db):
    """Selects the biggest highscore Value from all weekly habits"""
    cur = db.cursor()
    cur.execute("SELECT habits.name, MAX(highscore) FROM streak INNER JOIN habits ON streak.habitName = habits.name WHERE frequency = 'Weekly'")
    return cur.fetchone() 

def reset_streak(db, habitName):
    """Resets the streak value for a specific habit to 0"""
    cur = db.cursor()
    cur.execute("UPDATE streak SET currentstreak = 0 WHERE habitName = ?", (habitName,))
    db.commit()

def reset_streak_highscore(db, habitName):
    """Resets highscore and streak value to 0 for a specific habit"""
    cur = db.cursor()
    cur.execute("UPDATE streak SET currentstreak = 0, highscore = 0 WHERE habitName = ?", (habitName,))
    db.commit()    

def get_habit_last_checked(db):
    """Selects name, frequency, and last checked value from all habits"""
    cur = db.cursor()
    cur.execute("SELECT name, frequency, last_checked FROM habits")
    return cur.fetchall() 

def get_start_date(db, name):
    """Selects the start date for a specific habit"""
    cur = db.cursor()
    cur.execute("SELECT start FROM habits WHERE name = ?", (name,))
    return cur.fetchone()    

def update_name(db, old_name, new_name):
    """Updates the name for a habit in the habit table and streak table"""
    cur = db.cursor()
    cur.execute("UPDATE habits SET name = ? WHERE name = ?", (new_name, old_name,))
    cur.execute("UPDATE streak SET habitName = ? WHERE habitName = ?", (new_name, old_name))
    db.commit()

def update_streak_to_daily(db, name):
    """Changes the frequency to Daily"""
    cur = db.cursor()
    cur.execute("UPDATE habits SET frequency = 'Daily' WHERE name = ?", (name,))
    db.commit()    

def update_streak_to_weekly(db, name):
    """Changes the frequency to Weekly"""
    cur = db.cursor()
    cur.execute("UPDATE habits SET frequency = 'Weekly' WHERE name = ?", (name,))
    db.commit()      

def habit_exists(db, name):
    """Checks if there are entries for a specific habit, e.g. if the habit exists in the db"""
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM habits WHERE name = ?", (name,))
    count = cur.fetchone()[0]
    return count > 0

def last_checked_reset(db, name):
    cur = db.cursor()
    cur.execute("UPDATE habits SET last_checked = 'Not Checked' WHERE name =?", (name,))
    db.commit()

def delete_habit(db, name):
    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE name =?", (name,))
    cur.execute("DELETE FROM streak WHERE habitName =?", (name,))
    db.commit()        

  