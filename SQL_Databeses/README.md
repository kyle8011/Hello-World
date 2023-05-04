# Overview

I found that a lot of jobs are looking for experience with SQL so I figured I would give it a try.

The SQL.py file was more of a testing pad for implementing the database into the RPG2.py file. Just pressing run on the SQL.py file will test the different function and capabilities of SQLlite such as creating a table, editing values, removing values, and deleting things from the table. It reads from the tables created and uses an aggregate count function to count the number of items with a specific type in one of the tables. The RPG2.py file is something that I had written previously but did not have a way to save and read data from memory, which is exactly what the SQL database provided. I implemented the function that I wrote in RPG2.py to save character information and item information which can be loaded at a later time. The program is similar to other videogames, use the mouse to click on options then move with w-a-s-d or arrow keys and attack with the left mouse button and use abilities with the e button.

The ultimate purpose of this software is to incorporate saving and loading data into a video game.

[Software Demo Video](https://youtu.be/cZ6m7w1tRB0)

# Relational Database

Tables are organized into rows and columns that are all related by the key, in this case the name is being used as the key to tell what values apply in each case. The key is the same for both character stats and items that are affiliated with that character, thus, two or more tables can be used to  keep track of everything that needs to apply to a specific character.


The two tables that I made for this game are shown here. I put example values for what data might be placed inside the tables.

## Character Table
|name |type |level|xp   |health |damage |speed  |defense|ability|mana   |gold |
|:---:|:---:|:---:|:---:| :---: |:---:  |:---:  |:---:  |:---:  |:---:  |:---:|
|Kyle |"Mage"|1   |0    |100    |5      |2      |4      |5      |4      |100  |
|John |"Warrior"|4|12   |180    |13     |3      |21     |3      |4      |1000 |
...

## Item Table
|name|type|damage|defense|health|mana|ability|speed|level|equipped|
|:---:|:---:|:---:|:---: |:---: |:---:|:---: |:---:|:---:|:---:   |
|Kyle |"wand"|3   |0     |0     |2    |5     |0    |1    |True    |
|Kyle |"bow" |5   |1     |0     |0    |0     |5    |2    |False   |
|John |"sword"|7  |3     |0     |0    |0     |2    |4    |True    |
...

# Development Environment

Python is not the quickest programming language for running applications, but it will run most databases without delay and is very easy for the user to manipulate and find bugs in the code. There is also an sqlite library already written that has adapted it to python which I was able to import. For these reasons I chose to use python to develop this software.

For the SQL database development I used the python sqlite3 library along with the random library to generate data to put into the tables (the libraries for the game included pygame, time, and math as well). Sqlite3 has the same commands as normal SQL but the function calls look a little different. Before doing anything you need to connect to the database and create a cursor, then use the .execute() cursor method with your command in a string to perform any changes to the table. Afterward make sure to save changes and close the connection with the .commit() and .close() connection methods. 



# Useful Websites

- [sqlitetutorial](https://www.sqlitetutorial.net/sqlite-aggregate-functions/)
- [w3schools](https://www.w3schools.com/sql/sql_create_db.asp) This was the most useful for finding how to use SQL functions
- [python.org](https://docs.python.org/3.8/library/sqlite3.html)
- [tutorialspoint](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)
- [wikipedia](https://en.wikipedia.org/wiki/Relational_database) This helps to understand what a relational database is


# Future Work

- Add a third database holding current status information.
- On character load, maximize health and mana after items are equipped  rather than before.