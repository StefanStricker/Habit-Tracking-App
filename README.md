# Habit Tracker Application 

## Objective
This habit tracker application provides an easy and convenient way to keep track of the progress of implementing habits in day-to-day life. The program is accessed and managed over a command line interface on any operating system. 

In this application, users can create new habits they want to implement in their life and keep track of achievements through increasing streaks and high scores. This is achieved by checking off a habit in a given periodicity (e.g. daily or weekly). For example, the streak increases for a daily habit, if the habit has been checked off for two consecutive days in a row and will be reset if a day has been missed. Habits can also be analyzed and edited, and there is also an option to insert Mock-Data to test all functionalities (This Mock-Data can also be deleted without it interfering with manually created habits)

## Installation manual:

1 - git clone https://github.com/StefanStricker/Habit-Tracking-App.git

2 - cd Habit-Tracker-App

3 - pip install -r requirements.txt

## Run the Application
python main.py

## Remove all habits // Remove database
rm main.py

## Usage:
After starting the program the user Menu appears where the user has 6 different options to choose from:

1 - Create new habit

2 - Check off habit

3 - Modify habits

4 - Analyse

5 - Insert or Delete Mock Data

6 - Exit


1 - Create a new habit:
Creating a new habit is very easy. Upon choosing this option, you can write the name of the new habit to be created and then choose a periodicity, either Daily or Weekly in which you want to check off the habit, e.g. complete the task. After entering this information, name, and periodicity, the habit is stored in the database

2 - Checking off a habit
If you want to Check off a habit you simply have to write out its name. Daily habits can only be checked off once a day, and weekly habits can only be checked off once a week. If you check off a habit the streak gets increased by one. If you miss checking off the habit in time the streak will be reset to 0.

3 - Modify habits
The program will ask you for the name of the habit you want to modify. After entering its name you have to choose between Changing the name, changing the frequency, or deleting the habit. If the frequency of a habit gets changed the streak and high score will be reset to 0.

4 - Analyse
In the Analyse module, you have different options to choose from. You can analyze every habit in the database specifically and display streak and high score values, or you can see your top high scores from all habits overall.

5 - Insert or Delete Mock Data
Here you have the option to Insert or Delete Mock-Data to explore the functionalities. Mock Data can be deleted at any time without it affecting manually created habits.

6 - Exit
Exit the program

## Run Tests:
pytest .
