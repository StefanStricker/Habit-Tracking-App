import questionary
from db import get_db, get_habit_data, update_name, update_streak_to_daily, update_streak_to_weekly, reset_streak_highscore, habit_exists, last_checked_reset, delete_habit
from habit import dbHabit
from analyse import count_habits, count_daily_habits, count_weekly_habits, daily_habits_streaks, weekly_habits_streaks, best_daily_highscore, best_weekly_highscore, specific_highscore, current_streak, print_start
from mock_data import delete_mock_data, create_mock_data
import sqlite3

def cli():
    db = get_db()

    #reviews all habits if a check off has been missed and resets streaks accordingly at the start of the application
    dbHabit.review_all_habits(db)


    stop = False
    while not stop:
        #Main User Menu to navigate between: Create new habit, Check off habit, Modify habits, Analyse, Exit
        choice = questionary.select(
            "User Menu",
            choices=["Create new habit", "Check off habit", "Modify habits", "Analyse", "Insert or Delete Mock Data", "Exit"]
        ).ask()

        #Create a new habit and stores it in database
        if choice == "Create new habit":
            name = questionary.text("What is the name of the new habit?").ask()
            frequency = questionary.select("Do you want to check off this habit daily or weekly?", choices=["Daily", "Weekly"]).ask()
            last_checked = None
            if habit_exists(db, name):
                print("A habit with the same name already exists. Please choose a different name.")
            else:    
                habit = dbHabit(name, frequency, last_checked)
                habit.store(db)

        #Check off habit and updates streak and last checked value        
        elif choice == "Check off habit":
            habit_name = questionary.text("Write the name of the habit you want to check off").ask()
            habit_data = get_habit_data(db, habit_name)
            if habit_data is not None:
                habit_frequency = habit_data[1] 
                last_checked = habit_data[2]  
                habit = dbHabit(habit_name, habit_frequency, last_checked=last_checked)
                habit.check(db)
            else:
                print("ERROR: Habit not found in the database.")    

        #Change the name or the frequency of a habit, if frequency gets changed, highscore and streak value gets reset to 0        
        elif choice == "Modify habits":
            habit_name = questionary.text("Write the name of the habit you want to modify").ask()
            habit_data = get_habit_data(db, habit_name)
            if habit_data is not None:
                habit_frequency = habit_data[1] 
            else:
                print("ERROR: Habit not found in the database.") 
                continue   

            choice = questionary.select(
                "What do you want to modify?",
                choices=["Change name", "Change frequency", "Delete habit"]
            ).ask()

            if choice == "Change name":
                new_name = questionary.text("Write the new name for this habit").ask()
                update_name(db, habit_name, new_name)
                print(f"Habit name changed to: {new_name}")
            if choice == "Change frequency":
                choice = questionary.select(
                    "Are you sure you want to change the frequency? Your streak and highscore will be reset permanently!", 
                    choices= ["Yes", "No"]
                ).ask()

                if choice == "No":
                    print("Frequency NOT changed")
                if choice == "Yes":
                    if habit_frequency == "Daily":
                        update_streak_to_weekly(db, habit_name)
                        reset_streak_highscore(db, habit_name)
                        last_checked_reset(db, habit_name)
                        
                    if habit_frequency == "Weekly":
                        update_streak_to_daily(db, habit_name)
                        reset_streak_highscore(db, habit_name)
                        last_checked_reset(db, habit_name)

            if choice == "Delete habit":
                delete_habit(db, habit_name)   
                print(f" habit: {habit_name} deleted")         

        #Analyze habit data
        elif choice == "Analyse":
            count = count_habits(db)
            print(f"You have {count} habits")
            print(f"You have {count_daily_habits(db)} daily habits")
            print(f"You have {count_weekly_habits(db)} weekly habits")

            choice = questionary.select(
                "What would you like to do?",
                choices=["Show all daily habits & streak", "Show all weekly habits & streak", "Show highscores", "Analyze specific habit stats", "Return to User Menu"]
            ).ask()

            if choice == "Show all daily habits & streak":
                daily_habits_streaks(db)

            elif choice == "Show all weekly habits & streak":
                weekly_habits_streaks(db)

            elif choice == "Show highscores":    
                best_daily_highscore(db)
                best_weekly_highscore(db)

            #takes user input and displays specific habit stats: current streak, highscore, creation date
            elif choice == "Analyze specific habit stats":
                habit_name = questionary.text("Write the name of the habit you want to analyze").ask()
                habit_data = get_habit_data(db, habit_name)
                if habit_data is not None:
                    current_streak(db, habit_name)
                    specific_highscore(db, habit_name)
                    print_start(db, habit_name)
                    
                else:
                    print("ERROR: Habit not found in the database.")

            if choice == "Return to User Menu":
                continue       

        elif choice == "Insert or Delete Mock Data":
            db = sqlite3.connect("main.db")
            choice = questionary.select(
                "Would you like to Insert or Delete the Mock data?",
                choices=["Insert Mock Data", "Delete Mock Data", "Return to User Menu"]
            ).ask() 

            if choice == "Insert Mock Data":
                create_mock_data(db)
                print("Mock Data Inserted")

            elif choice == "Delete Mock Data":
                delete_mock_data(db)  
                print("Mock Data deleted")     

            elif choice == "Return to User Menu":
                continue       

        #Exits the applicaton    
        elif choice == "Exit":
            print("Good bye!")
            db.close()
            stop = True        
        else:
            print("Good bye error!!")
            stop = True 
          

if __name__ == "__main__":
    cli()
