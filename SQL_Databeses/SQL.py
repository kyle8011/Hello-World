import sqlite3 as SQL
import random

def main():
    # Random stat generator
    stats = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(stats)):
        stats[i] = random.randint(1, 10)
    # Random name selector
    names = ["Kyle", "Shawn", "Phillip", "Pam", "Doug", "Cristi", "Jenny", "Kathy", "Teresa"]
    rand_name = random.choice(names)
    # Random class selection
    classes = ["Warrior", "Mage", "Archer"]
    rand_class = random.choice(classes)
    add_new_character_data(rand_name, rand_class)
    get_table("characters")
    edit_character_data(rand_name, stats)
    get_table("characters")
    
    print("Getting character data")
    data = get_character_data(rand_name)
    for x in data:
        print(f"{x}")
    
    delete_character(rand_name)
    get_table("characters")
    

    # Create items list to append
    items_list = [["sword", 5, 3, 0, 0, 0, 0, 1, False],
                  ["shield", 0, 3, 10, 0, 0, 0, 2, True],
                  ["wand", 5, 0, 0, 2, 2, 0, 3, True],
                  ["bow", 5, 0, 0, 0, 0, 0, 4, False],
                  ["helmet", 0, 3, 5, 0, 0, 0, 5, True],
                  ["necklace", 0, 1, 2, 2, 2, 0, 6, False],
                  ["boots", 0, 3, 10, 0, 0, 0, 7, False],
                  ["pants", 0, 3, 10, 0, 0, 0, 8, True]]
    update_items(rand_name, items_list)
    print("This is every item in the database")
    get_table("items")

    count_items("sword")

def get_character_data(name):
    con = SQL.connect('SQL_Database/player.db')
    cur = con.cursor()
    data = 'none'

    if(check_for_table(cur, "characters") == False):
        print("No character data available")
    else:
        # Check to make sure the name is in the table
        for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
            if name in names:
                cur.execute(f"SELECT * FROM characters WHERE name='{name}'")
                data = cur.fetchall()[0]
    return data

def get_item_data(name):
    con = SQL.connect('SQL_Database/player.db')
    cur = con.cursor()
    data = 'none'

    if(check_for_table(cur, "items") == False):
        print("No item data available")
    else:
        # Check to make sure the name is in the table
        for names in cur.execute(f"SELECT name FROM items ORDER BY name"):
            if name in names:
                cur.execute(f"SELECT * FROM items WHERE name='{name}'")
                data = cur.fetchall()[0]
    return data

def delete_character(name):
    con = SQL.connect('SQL_Database/player.db')
    cur = con.cursor()

    if(check_for_table(cur, "characters") == False):
        print("No character data available")
    else:
        # Check to make sure the name is in the table
        for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
            if name in names:
                print(f"'{name}' deleted")
                cur.execute(f"DELETE FROM characters WHERE name = '{name}'")
        for names in cur.execute(f"SELECT name FROM items ORDER BY name"):
            if name in names:
                cur.execute(f"DELETE FROM items WHERE name = '{name}'")
    con.commit()
    con.close()


def edit_character_data(character_name, stats):
    con = SQL.connect('SQL_Database/player.db')
    cur = con.cursor()
    print(f"Editing {character_name} in table")

    # Check if there is a table
    if(check_for_table(cur, "characters") == False):
        print("No data in table")
    else:
        for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
            #print(names)
            for name in names:
                if name == character_name:
                    cur.execute(f"UPDATE characters SET level = {stats[0]}, xp = {stats[1]}, health = {stats[2]}, damage = {stats[3]}, speed = {stats[4]}, defense = {stats[5]}, ability = {stats[6]}, mana = {stats[7]}, gold = {stats[8]} WHERE name = '{character_name}'")
                    print("Update Successful")

    con.commit()
    con.close()



def get_table(table_name):
    con = SQL.connect('SQL_Database/player.db')
    cur = con.cursor()
    print("Checking table")
    table = []

    # Checking if there is a table with that name
    if(check_for_table(cur, f"{table_name}") == False):
        print("No table with that name")
    else:
        for row in cur.execute(f"SELECT * FROM '{table_name}' ORDER BY name"):
            table.append(row)
            print(row)
    con.close()
    return table


def add_item_to_database(name, item, cur):

    # Checking if there is already a table
    if(check_for_table(cur, "items") == False):
        # If not, create a new items table
        cur.execute("CREATE TABLE items (name, type, damage, defense, health, mana, ability, speed, level, equipped)")

    # Adding the values to the characters table
    cur.execute(f"INSERT INTO items VALUES ('{name}', '{item[0]}', {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}, {item[6]}, {item[7]}, {item[8]})")


def update_items(name, items_list):
    con = SQL.connect('SQL_Database/player.db')
    cur = con.cursor()

    if(check_for_table(cur, "items") == False):
        for x in range(len(items_list)):
            add_item_to_database(name, items_list[x], cur)
        print("No item data available")
    
    # Check to make sure the name is in the table
    for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
        if name in names:
            # Delete each item previously associated
            cur.execute(f"DELETE FROM items WHERE name = '{name}'")
            # Add each item given in the list
            for x in range(len(items_list)):
                add_item_to_database(name, items_list[x], cur)
            con.commit()
    con.close()


def add_new_character_data(name, type):
    con = SQL.connect('SQL_Database/player.db')
    cur = con.cursor()
    already_taken = False

    # Checking if there is already a table
    if(check_for_table(cur, "characters") == False):
        # If not, create a new characters table
        cur.execute("CREATE TABLE characters (name, type, level, xp, health, damage, speed, defense, ability, mana, gold)")
    
    # Check to make sure the name is not already taken
    for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
        if name in names:
            already_taken = True
            print(f"Name '{name}' already taken")

    if already_taken == False:
        print(f"Adding {name} to table")
        # Creating a new character
        stats = ["name", "type", "level", "health", "damage", "speed", "defense", "ability", "mana"]
        Warrior_stats = [150, 20, 2, 3, 2, 1] # Health, damage, attack speed, defense, ability, mana 
        Mage_stats =    [100, 20, 2, 1, 5, 3]
        Archer_stats =  [100, 25, 3, 1, 3, 2]
        if type == "Archer":
            stats = Archer_stats
        if type == "Warrior":
            stats = Warrior_stats
        if type == "Mage":
            stats = Mage_stats

        # Adding the values to the characters table
        cur.execute(f"INSERT INTO characters VALUES ('{name}', '{type}', 1, 0, {stats[0]}, {stats[1]}, {stats[2]}, {stats[3]}, {stats[4]}, {stats[5]}, 0)")

        con.commit()
    con.close()
    return already_taken

def check_for_table(cur, table_name):
    cur.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cur.fetchone()[0] < 1:
        return False
    else:
        return True
    
# Aggregate function
def count_items(item_name):
    con = SQL.connect('SQL_Database/player.db')
    cur = con.cursor()

    cur.execute(f"SELECT count(*) FROM items WHERE type='{item_name}'")
    print(f"There are {cur.fetchall()[0][0]} items named {item_name} in the table")
    con.close()
    

if __name__ == "__main__":
    main()