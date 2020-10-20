'''
Created on Sep 27, 2020

@author: Jason
'''
from clear import clear
import re
import getpass

pw = ""

# Test against current password, or prompt for new one
def enterPassword():
    global pw
    if pw == "":
        isPasswordOK()
        return
    else:
        login = getpass.getpass("Enter password: ")
        if login == pw:
            return True
        else:
            print("Password incorrect.")
            return False

# Test password strength based on multiple factors
def isPasswordOK():
    global pw
    pwstr = 0
    
    # Must match 4 out of 5 categories to be accepted
    while pwstr < 4:
        clear()
        newpw = getpass.getpass("Please enter a new password for your first login: ")
        
        if len(newpw) < 8:
            print("Password shorter than 8 characters!")
        else:
            pwstr += 1
        if re.search('[a-z]', newpw) == None:
            print("Missing lowercase letters!")
        else:
            pwstr += 1
        if re.search('[A-Z]', newpw) == None:
            print("Missing uppercase letters!")
        else:
            pwstr += 1
        if re.search('[0-9]', newpw) == None:
            print("Missing numerals!")
        else:
            pwstr += 1
        if re.search('[!@#$%^&*]', newpw) == None:
            print("Missing special characters! ! @ # $ % ^ & *")
        else:
            pwstr += 1
            
        if pwstr < 4:
            print("Password strength too low. Please try again.")
            pwstr = 0
        else:
            print("Password accepted! Please do not forget it.")
            pw = newpw
