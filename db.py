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
        creationdate TEXT,
        currentstreak INT DEFAULT 0,
        highscore INT DEFAULT 0,
        habitName TEXT,
        FOREIGN KEY (habitName) REFERENCES habits(name))""")    
    
    db.commit()   
    
     

def add_habit(db, name, frequency, last_checked="Not Checked"):
    cur = db.cursor()
    cur.execute("INSERT OR IGNORE INTO habits VALUES (?, ?, ?, ?)", (name, frequency, last_checked, date.today()))
    db.commit()

    cur.execute("INSERT OR IGNORE INTO streak (creationdate, currentstreak, habitName) VALUES (?, ?, ?)",(date.today(), 0, name))
    db.commit()

def check_off(db, habitName):
    cur = db.cursor()
    cur.execute("UPDATE streak SET currentstreak =  currentstreak + 1 WHERE habitName = ?", (habitName,))
    cur.execute("UPDATE habits SET last_checked = ? WHERE name = ?", (date.today(), habitName))
    db.commit()

def all_habits(db):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
    return cur.fetchall()

def daily_habits(db):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE frequency = 'Daily'")
    return cur.fetchall()

def weekly_habits(db):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE frequency = 'Weekly'")
    return cur.fetchall()

def get_daily_names_streaks(db):
    cur = db.cursor()
    cur.execute("SELECT habits.name, streak.currentstreak FROM habits INNER JOIN streak ON habits.name = streak.habitName WHERE frequency = 'Daily'")
    return cur.fetchall()

def get_weekly_names_streaks(db):
    cur = db.cursor()
    cur.execute("SELECT habits.name, streak.currentstreak FROM habits INNER JOIN streak ON habits.name = streak.habitName WHERE frequency = 'Weekly'")
    return cur.fetchall()

def get_highest_daily_streak(db):
    cur = db.cursor()
    cur.execute("SELECT MAX(currentstreak) FROM streak INNER JOIN habits ON habitName = habits.name WHERE habits.frequency = 'Daily'")
    return cur.fetchone()

def get_highest_weekly_streak(db):
    cur = db.cursor()
    cur.execute("SELECT MAX(currentstreak) FROM streak INNER JOIN habits ON habitName = habits.name WHERE habits.frequency = 'Weekly'")    
    return cur.fetchone()

def currstreak(db, habitName):
    cur = db.cursor()
    cur.execute("SELECT currentstreak FROM streak WHERE habitName = ?", (habitName,))
    return cur.fetchone()
    
def get_habit_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE name = ?", (name,))
    return cur.fetchone()    

def get_highscore(db, habitName):
    cur = db.cursor()
    cur.execute("SELECT highscore FROM streak WHERE habitName = ?", (habitName,))
    return cur.fetchone()    

def new_highscore(db, habitName):
    cur = db.cursor()
    cur.execute("UPDATE streak SET highscore = currentstreak WHERE habitName = ?", (habitName,))
    db.commit()

def get_daily_highscore(db):
    cur = db.cursor()
    cur.execute("SELECT habits.name, MAX(highscore) FROM streak INNER JOIN habits ON streak.habitName = habits.name WHERE frequency = 'Daily'")
    return cur.fetchone() 

def get_weekly_highscore(db):
    cur = db.cursor()
    cur.execute("SELECT habits.name, MAX(highscore) FROM streak INNER JOIN habits ON streak.habitName = habits.name WHERE frequency = 'Weekly'")
    return cur.fetchone() 

def reset_streak(db, habitName):
    cur = db.cursor()
    cur.execute("UPDATE streak SET currentstreak = 0 WHERE habitName = ?", (habitName,))
    db.commit()

def reset_streak_highscore(db, habitName):
    cur = db.cursor()
    cur.execute("UPDATE streak SET currentstreak = 0, highscore = 0 WHERE habitName = ?", (habitName,))
    db.commit()    

def get_habit_last_checked(db):
    cur = db.cursor()
    cur.execute("SELECT name, frequency, last_checked FROM habits")
    return cur.fetchall() 

def get_start_date(db, name):
    cur = db.cursor()
    cur.execute("SELECT start FROM habits WHERE name = ?", (name,))
    return cur.fetchone()    

def update_name(db, old_name, new_name):
    cur = db.cursor()
    cur.execute("UPDATE habits SET name = ? WHERE name = ?", (new_name, old_name,))
    cur.execute("UPDATE streak SET habitName = ? WHERE habitName = ?", (new_name, old_name))
    db.commit()

def update_streak_to_daily(db, name):
    cur = db.cursor()
    cur.execute("UPDATE habits SET frequency = 'Daily' WHERE name = ?", (name,))
    db.commit()    

def update_streak_to_weekly(db, name):
    cur = db.cursor()
    cur.execute("UPDATE habits SET frequency = 'Weekly' WHERE name = ?", (name,))
    db.commit()      

def habit_exists(db, name):
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM habits WHERE name = ?", (name,))
    count = cur.fetchone()[0]
    return count > 0
