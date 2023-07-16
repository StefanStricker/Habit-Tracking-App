from db import delete_habit
import sqlite3

db = sqlite3.connect("main.db")

def create_mock_data(db):
    """Insert mock data into the database"""
    with db:
        cursor = db.cursor()
        cursor.executemany(
            "INSERT INTO habits (name, frequency, last_checked, start) VALUES (?, ?, ?, ?)",
            [
                ("Meditation", "Daily", "2023-07-16", "2023-06-01"),
                ("Going to the Gym", "Weekly", "2023-07-14", "2023-04-17"),
                ("Reading", "Daily", "2023-07-12", "2023-06-06"),
                ("Cooking", "Daily", "2023-07-16", "2023-05-07"),
                ("Go out with friends", "Weekly", "2023-07-08", "2023-07-08"),
                ("Learning", "Daily", "2023-07-15", "2023-03-22"),
                ("Cleaning", "Weekly", "2023-07-01", "2023-06-12"),
            ]
        )
        db.commit()

        cursor.executemany(
            "INSERT INTO streak (currentstreak, highscore, habitName) VALUES (?, ?, ?)",
            [
                ("4", "13", "Meditation"),
                ("1", "2", "Going to the Gym"),
                ("6", "6", "Reading"),
                ("5", "12", "Cooking"),
                ("0", "1", "Go out with friends"),
                ("12", "12", "Learning"),
                ("7", "7", "Cleaning"),
            ]
        )
        db.commit()                       


def delete_mock_data(db):
    """Deletes mock data"""
    delete_habit(db, "Meditation")
    delete_habit(db, "Going to the Gym")
    delete_habit(db, "Reading",)
    delete_habit(db, "Cooking")
    delete_habit(db, "Go out with friends")
    delete_habit(db, "Learning")
    delete_habit(db, "Cleaning")
          