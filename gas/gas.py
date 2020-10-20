import mysql.connector

from clear import clear
from Service import Service
from Order import Order
from Login import enterPassword

services = []
orders = []

# Connect to local DB
try:
    conn = mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        database='gas')
except mysql.connector.Error as err:
    print("Problem connecting to MySQL server: {}".format(err))
    exit()

# Cursor for manipulating DB
cursor = conn.cursor()

# Build service and order lists to avoid extra DB hits
def buildLists():
    global services
    services = []
    global orders
    orders = []
    
    # Query DB for all services
    query = "SELECT * FROM services;"
    cursor.execute(query)
    
    # Create list of Service objects from results (TODO: by column names)
    for result in cursor:
        services.append(Service(
            result[0],
            result[1],
            result[2],
            result[3]))
    
    # Do the same for orders
    query = "SELECT * FROM orders;"
    cursor.execute(query)
    
    for result in cursor:
        orders.append(Order(
            result[0],
            result[1],
            result[2]))

# Small wrapper for sending SQL queries
def sqlIt(query):
    try:
        cursor.execute(query)
    # Fail outright on MySQL error
    except Exception as e:
        print("MySQL error: {}".format(e))
        conn.close()
        exit()
    # Do not commit changes if problem occurs, but don't crash
    if cursor.fetchwarnings():
        print(cursor.fetchwarnings())
        return
    else:
        conn.commit()
        buildLists()
        raw_input("Completed successfully. (press enter to continue)")
        return

##########

# Create new order entry
def placeOrder():
    # Display all services
    print("Current offerings: ")
    displayAllServices()
    print('''
    ============================
    PLACE YOUR ORDER
    ============================
    ''')
    
    # Loop until customer is done
    moreservices = "y"
    while moreservices == "y":
        # Choose a service
        snum = searchServices()
        if snum == -1:
            return
        quantity = 0
        # Choose quantity
        while quantity == 0:
            try:
                quantity = int(raw_input("Quantity of service: "))
            except ValueError:
                print "Please enter an integer"
                quantity = 0
                pass
        # Create entry
        query = "INSERT INTO orders VALUES ({}, {}, {});".format(0, snum, quantity)
        sqlIt(query)
        # More?
        moreservices = raw_input("\nPlace another order? (y, n)")
        if moreservices != "y":
            return
        
##########

# Customer calculator for gas fees
def gasFeeCalculation():
    gallons = 0
    charge = 0.0
    fee = 15
    costUpTo6K = 2.35
    costUpTo20K = 3.75
    costOver20K = 6.00
    
    clear()
    
    while gallons == 0:
        try:
            gallons = int(raw_input("Enter total gallons used, divided by 1000 (rounded up): "))
        except ValueError:
            print "Please enter an integer"
            gallons = 0
            pass
    
    # Each tier of gas costs a different amount, going up as the amount rises
    #   e.g. 10 gallons = 6 gallons at UpTo6K rate, 4 gallons at UpTo20K rate
    if gallons > 20:
        charge = (gallons - 20) * costOver20K
        charge += 14 * costUpTo20K
        charge += 6 * costUpTo6K
    elif gallons > 6 and gallons <= 20:
        charge = (gallons - 6) * costUpTo20K
        charge += 6 * costUpTo6K
    else:
        charge = gallons * costUpTo6K

    print('''

    You have used {} thousand gallons of gasoline.
    Your total gas bill is:
        ${:.2f} USD

    '''.format(gallons, charge + fee))
    raw_input("(press enter to return)")

##########

# Display all existing orders
def showOrders():
    global orders
    clear()
    print('''
    ====================================================
    NO.\t\tSERVICE NUMBER\t\tQUANTITY
    ====================================================''')
    for o in orders:
        o.showOrderList()

# Remove orders
def deleteOrder():
    global orders
    
    # Get order number
    delorder = int(raw_input("Enter order number: "))
    if delorder == 0:
        return 
    
    # Check each order for matching number
    for o in orders:
        if o.number == delorder:
            o.showOrder()
            deleteconf = str(raw_input("Delete this order? (y, n)"))
            if deleteconf != "y":
                return 
            query = "DELETE FROM orders WHERE number = {};".format(delorder)
            sqlIt(query)
            return
    raw_input("Could not find order. (press enter to continue)")
    return

# Create new service
def createService():
    name = ""
    price = -1.0
    discount = -1
    
    while name == "":
        try:
            name = str(raw_input("Please enter the service name: "))
        except ValueError:
            print "Please enter a valid name"
            name = ""
    
    while price == -1.0:
        try:
            price = float(raw_input("Please enter the price (USD): "))
        except ValueError:
            print "Please enter a value numeric value"
            price = -1.0
    
    while discount == -1:
        try:
            discount = int(raw_input("Please enter the discount (%): "))
        except ValueError:
            print "Please enter an integer value"
            discount = -1
    
    # Commit new entry
    query = "INSERT INTO services VALUES (0, '{}', {}, {});".format(
        name,
        price,
        discount)
    sqlIt(query)    

##########

# Update existing service
def modifyService():
    # Request service to modify
    number = searchServices()
    if number == -1:
        return

    name = ""
    price = -1.0
    discount = -1

    while name == "":
        try:
            name = str(raw_input("Please enter the service name: "))
        except ValueError:
            print "Please enter a valid name"
            name = ""
    
    while price == -1.0:
        try:
            price = float(raw_input("Please enter the price (USD): "))
        except ValueError:
            print "Please enter a value numeric value"
            price = -1.0
    
    while discount == -1:
        try:
            discount = int(raw_input("Please enter the discount (%): "))
        except ValueError:
            print "Please enter an integer value"
            discount = -1
    
    # Commit changes
    query = "UPDATE services SET service_name='{}', price={}, discount={} where service_number={};".format(
        name,
        price,
        discount,
        number)
    sqlIt(query)

##########

# Remove services
def deleteService():
    number = searchServices()
    # TODO: Error handling, verification
    if number == -1:
        return
    query = "DELETE FROM services WHERE service_number={}".format(number)
    sqlIt(query)

##########

# Display chart of services
def displayAllServices():
    global services
    clear()
    print('''
    ====================================================
    \t\tP.NO.\t\tNAME\t\tPRICE\t\tDISCOUNT
    ====================================================''')
    for s in services:
        s.showServiceList()

##########

# Used for finding existing service; -1 on failure
def searchServices():
    snum = 0
    while snum == 0:
        try:
            snum = int(raw_input("\nPlease enter the service number: "))
        except ValueError:
            print "Please enter a valid number"
            snum = 0
            pass
    for s in services:
        if s.number == snum:
            s.showService()
            return snum
    raw_input("\nRequested service not found. (press enter to return)")
    return -1

##########

# Main menu for admins
def adminMenu():
    menuinput = 0
    while int(menuinput) != 9:
        clear()
        print('''
        Admin Menu:
        
        1. Create service
        2. Display all services
        3. Search services
        4. Gas service fee calculator
        5. Modify service
        6. Delete service
        7. Display all requests
        8. Remove request
        9. Return to main menu''')
        try:
            menuinput = int(raw_input("Select an option: "))
        except ValueError:
            print "Please enter a value from 1-8"
            pass
        if menuinput == 1:
            createService()
        elif menuinput == 2:
            displayAllServices()
        elif menuinput == 3:
            searchServices()
        elif menuinput == 4:
            gasFeeCalculation()
        elif menuinput == 5:
            modifyService()
        elif menuinput == 6:
            deleteService()
        elif menuinput == 7:
            showOrders()
        elif menuinput == 8:
            deleteOrder()

##########

if __name__ == '__main__':
    # Create lists of services and orders from SQL
    buildLists()
    
    # Loop until user enters '3' to quit
    menuinput = 0
    while int(menuinput) != 3:
        clear()
        print('''
        MAIN MENU
           
        1. Customer
        2. Administrator
        3. Quit

        ''')
        try:
            menuinput = int(raw_input("Select option: "))
        # Ignore anything but numerical 1-3 and repeat the menu
        except ValueError as e:
            print "\nPlease enter a value from 1-3"
            pass
        if menuinput == 1:
            # Place order
            placeOrder()
        elif menuinput == 2:
            # Only show admin menu after password validation
            valid = enterPassword()
            if valid == True:
                adminMenu()
            else:
                pass
    print "\nGoodbye!"
    # Close DB gracefully
    conn.close()
