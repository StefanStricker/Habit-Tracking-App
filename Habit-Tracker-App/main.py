import questionary
from db import get_db, get_habit_data, get_start_date
from habit import dbHabit
from analyse import count_habits, count_daily_habits, count_weekly_habits, daily_habits_streaks, weekly_habits_streaks, best_daily_highscore, best_weekly_highscore, specific_highscore, current_streak, print_start

def cli():
    db = get_db()

    dbHabit.review_all_habits(db)


    stop = False
    while not stop:
        choice = questionary.select(
            "User Menu",
            choices=["Create new habit", "Check off habit", "Modify habits", "Analyse", "Exit"]
        ).ask()

        if choice == "Create new habit":
            name = questionary.text("What is the name of the new habit?").ask()
            frequency = questionary.select("Do you want to check off this habit daily or weekly?", choices=["Daily", "Weekly"]).ask()
            last_checked = None
            habit = dbHabit(name, frequency, last_checked)
            habit.store(db)
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
        elif choice == "Modify habits":
            habit_name = questionary.text("Write the name of the habit you want to modify").ask()
            #Add feature
        elif choice == "Analyse":
            count = count_habits(db)
            print(f"You have {count} habits")
            print(f"You have {count_daily_habits(db)} daily habits")
            print(f"You have {count_weekly_habits(db)} weekly habits")

            choice = questionary.select(
                "What would you like to do?",
                choices=["Show all daily habits & streak", "Show all weekly habits & streak", "Show highscores", "Analyze specific habit stats"]
            ).ask()

            if choice == "Show all daily habits & streak":
                daily_habits_streaks(db)

            elif choice == "Show all weekly habits & streak":
                weekly_habits_streaks(db)

            elif choice == "Show highscores":    
                best_daily_highscore(db)
                best_weekly_highscore(db)

            elif choice == "Analyze specific habit stats":
                habit_name = questionary.text("Write the name of the habit you want to analyze").ask()
                habit_data = get_habit_data(db, habit_name)
                if habit_data is not None:
                    current_streak(db, habit_name)
                    specific_highscore(db, habit_name)
                    print_start(db, habit_name)
                    
                else:
                    print("ERROR: Habit not found in the database.")
                
            
        elif choice == "Exit":
            print("Good bye!")
            stop = True        
        else:
            print("Good bye!")
            stop = True 
          

if __name__ == "__main__":
    cli()
