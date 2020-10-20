'''
Created on Oct 5, 2020

@author: Jason
'''

from animalData import animalData
from habData import habData
import mysql.connector

# Connect to local MySQL database (running in Docker)
conn = mysql.connector.connect(
    user='root',
    password='root',
    host='127.0.0.1',
    database='zoo')

# MySQL cursor
cursor = conn.cursor()

# Animal and habitat storage
animalList = []
habList = []

# Retrieve latest table contents from MySQL
#   Unless something changes, use this data to reduce DB hits
def rebuildLists():
    global animalList
    animalList = []
    global habList
    habList = []
    
    query = "SELECT * FROM animals;"
    cursor.execute(query)
    
    # Retrieve animal info by DB order (TODO: by column_names)
    for result in cursor:
        animalList.append(animalData(
            result[0],
            result[2], # Ordered species, name in DB
            result[1],
            result[3],
            result[4],
            result[5],
            result[6]))
    
    query = "SELECT * FROM habitats;"
    cursor.execute(query)
    
    for result in cursor:
        habList.append(habData(
            result[0],
            result[2], # Ordered species, name in DB
            result[1],
            result[3],
            result[4],
            result[5],
            result[6]))

##########

# Decision tree for animal info
def animalMenu():
    menuinput = 0
    while int(menuinput) != 5:
        print('''Choose an action:
        1. View animals
        2. Add animal
        3. Update animal
        4. Remove animal
        5. Return''')

        try:
            menuinput = int(input("Select option: "))
            if menuinput == 1:
                animalShow()
                pass
            if menuinput == 2:
                animalCreate()
                pass
            if menuinput == 3:
                animalUpdate()
                pass
            if menuinput == 4:
                animalDelete()
                pass
            if menuinput == 5:
                return 
        except ValueError:
            print("\nPlease enter a value from 1-{}".format(len(animalList)+1))
            pass
        except IndexError:
            print("\nPlease enter a value from 1-{}".format(len(habList)+1))
            pass

# Displays a list of available animals and returns selection
def animalGet():
    global animalList
    menuinput = 0
    # Loop until valid selection is made (all animals + return option)
    while int(menuinput) != len(animalList)+1:
        # Display all animals' names
        for x in range(len(animalList)):
            print("{}. {}".format(x+1, animalList[x].animalName))
        print("{}. Return".format(len(animalList)+1))
        try:
            menuinput = int(input("Select option: "))
            if menuinput == len(animalList)+1:
                return -1
            else:
                return (menuinput - 1)
        except ValueError:
            print("\nPlease enter a value from 1-{}".format(len(animalList)+1))
            pass
        except IndexError:
            print("\nPlease enter a value from 1-{}".format(len(habList)+1))
            pass

# Display individual animal's data and display alarms
def animalShow():
    global animalList
    show = animalGet()
    # animalGet() returns 0 on 'return'/'no selection'
    while show != -1:
        animalList[show].showAnimal()
        animalList[show].checkAlert()
        show = animalGet()

# Modify an existing animal's information
def animalUpdate():
    global animalList
    update = animalGet()
    if update != 0:
        # Update animal object with prompts
        animalList[update].updateAnimal()
        # Build query
        query = '''UPDATE animals SET age={},
            health='{}',
            feeding='{}',
            alarm={}
            WHERE id={};'''.format(animalList[update].animalAge,
                                   animalList[update].animalHealth,
                                   animalList[update].animalFeeding,
                                   animalList[update].animalAlarm,
                                   animalList[update].animalID)
        try:
            # Run query
            cursor.execute(query)
        except Exception as e:
            print("Error updating row: {}".format(e))
            conn.close()
            exit()
        if cursor.fetchwarnings():
            print(cursor.fetchwarnings())
        else:
            # Commit change if no warnings or errors detected
            conn.commit()
            print("Entry successfully updated.")
            rebuildLists()
    else:
        return

# Remove animal from the DB
def animalDelete():
    global animalList
    delete = animalGet()
    if delete != 0:
        query = '''DELETE FROM animals WHERE id={};'''.format(animalList[delete].animalID)
        try:
            cursor.execute(query)
        except Exception as e:
            print("Error deleting row: {}".format(e))
            conn.close()
            exit()
        if cursor.fetchwarnings():
            print(cursor.fetchwarnings())
        else:
            conn.commit()
            print("Entry successfully removed.")
            rebuildLists()
    else:
        return

# Create new animal (TODO: error checking)
def animalCreate():
    species = input("Enter species: ")
    name = input("Enter name: ")
    age = int(input("Enter age (years): "))
    health = input("Enter health: ")
    feeding = input("Enter feeding: ")
    alarm = int(input("Enter alarm (0: None, 1: Health, 2: Feeding): "))
    
    # No need to create animalData object, rebuildLists will so this later
    query = "INSERT INTO animals VALUES(0, '{}', '{}', {}, '{}', '{}', {});".format(
        name, species, age, health, feeding, alarm)
    try:
        cursor.execute(query)
    except Exception as e:
        print("Error adding row: {}").format(e)
        conn.close()
        exit()
    if cursor.fetchwarnings():
        print(cursor.fetchwarnings())
    else:
        conn.commit()
        print("Entry successfully added.")
        rebuildLists()

##########

# Decision tree for hab info
def habMenu():
    menuinput = 0
    while int(menuinput) != 5:
        print('''Choose an action:
        1. View habitats
        2. Add habitat
        3. Update habitat
        4. Remove habitat
        5. Return''')

        try:
            menuinput = int(input("Select option: "))
            if menuinput == 1:
                habShow()
                pass
            if menuinput == 2:
                habCreate()
                pass
            if menuinput == 3:
                habUpdate()
                pass
            if menuinput == 4:
                habDelete()
                pass
            if menuinput == 5:
                return 
        except ValueError:
            print("\nPlease enter a value from 1-{}".format(len(habList)+1))
            pass
        except IndexError:
            print("\nPlease enter a value from 1-{}".format(len(habList)+1))
            pass

# Displays a list of available habs and returns selection
def habGet():
    global habList
    menuinput = 0
    # Loop until valid selection is made (all habs + return option)
    while int(menuinput) != len(habList)+1:
        # Display all habs by titles
        for x in range(len(habList)):
            print("{}. {}".format(x+1, habList[x].habTitle))
        print("{}. Return".format(len(habList)+1))
        try:
            menuinput = int(input("Select option: "))
            if menuinput == len(habList)+1:
                return -1
            else:
                return (menuinput - 1)
        except ValueError:
            print("\nPlease enter a value from 1-{}".format(len(habList)+1))
            pass
        except IndexError:
            print("\nPlease enter a value from 1-{}".format(len(habList)+1))
            pass

# Display individual hab's data and display alarms
def habShow():
    global habList
    show = habGet()
    # habGet() returns -1 on 'return'/'no selection'
    while show != -1:
        habList[show].showHabitat()
        habList[show].checkAlert()
        show = habGet()

# Modify an existing hab's information
def habUpdate():
    global habList
    update = habGet()
    if update != 0:
        # Update hab object with prompts
        habList[update].updateHabitat()
        # Build query
        query = '''UPDATE habitats SET temperature='{}',
            feeding='{}',
            cleaning='{}',
            alarm={}
            WHERE id={};'''.format(habList[update].habTemp,
                                   habList[update].habFood,
                                   habList[update].habClean,
                                   habList[update].habAlert,
                                   habList[update].habID)
        try:
            # Run query
            cursor.execute(query)
        except Exception as e:
            print("Error updating row: {}".format(e))
            conn.close()
            exit()
        if cursor.fetchwarnings():
            print(cursor.fetchwarnings())
        else:
            # Commit change if no warnings or errors detected
            conn.commit()
            print("Entry successfully updated.")
            rebuildLists()
    else:
        return

# Remove hab from the DB
def habDelete():
    global habList
    delete = habGet()
    if delete != 0:
        query = '''DELETE FROM habitats WHERE id={};'''.format(habList[delete].habID)
        try:
            cursor.execute(query)
        except Exception as e:
            print("Error deleting row: {}".format(e))
            conn.close()
            exit()
        if cursor.fetchwarnings():
            print(cursor.fetchwarnings())
        else:
            conn.commit()
            print("Entry successfully removed.")
            rebuildLists()
    else:
        return

# Create new hab (TODO: error checking)
def habCreate():
    species = input("Enter species: ")
    habitat = input("Enter habitat title: ")
    temperature = input("Enter temperature info: ")
    feeding = input("Enter feeding info: ")
    cleaning = input("Enter cleaning info: ")
    alarm = input("Enter alarm (0: None, 1: Temp, 2, Feeding, 3: Cleaning): ")
    
    # No need to create habData object, rebuildLists will so this later
    query = "INSERT INTO habitats VALUES(0, '{}', '{}', '{}', '{}', '{}', {});".format(
        habitat, species, temperature, feeding, cleaning, alarm)
    try:
        cursor.execute(query)
    except Exception as e:
        print("Error adding row: {}".format(e))
        conn.close()
        exit()
    if cursor.fetchwarnings():
        print(cursor.fetchwarnings())
    else:
        conn.commit()
        print("Entry successfully added.")
        rebuildLists()

#####

if __name__ == '__main__':
    # Retrieve current animal and hab data from MySQL
    rebuildLists() 
  
    menuinput = 0
    while int(menuinput) != 3:
        #clear()
        print('''
        MAIN MENU:
        1. View animal list
        2. View habitat list
        3. Quit''')
        print("")
        try:
            menuinput = int(input("Select option: "))
        # Ignore anything but numerical 1-3 and repeat the menu
        except ValueError:
            print("\nPlease enter a value from 1-3")
            pass
        if menuinput == 1:
            animalMenu()
            pass
        if menuinput == 2:
            habMenu()
            pass
            
    print("\nGoodbye!")
