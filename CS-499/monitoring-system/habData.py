'''
Created on Oct 5, 2020

@author: Jason
'''

from popup import popup

class habData():
    '''
    classdocs
    '''

    habType = ""
    habTitle = ""
    habTemp = ""
    habFood = ""
    habClean = ""
    habAlert = 0
    habID = 0
    
    def showHabitat(self):
        print('''Habitat - {}
        Species type: {}
        Temperature: {}
        Food source: {}
        Cleanliness: {}
        
        '''.format(self.habTitle,
                   self.habType.capitalize(),
                   self.habTemp,
                   self.habFood,
                   self.habClean))
        
    def updateHabitat(self):
        self.habTemp = input("Enter temperature info: ")
        self.habFood = input("Enter feeding info: ")
        self.habClean = input("Enter cleaning info: ")
        self.habAlert = int(input("Enter alarm (0: None, 1: Temp, 2: Feeding, 3: Cleaning): "))

    def checkAlert(self):
        if self.habAlert == 1:
            popup("Temperature alert!\nThe {} is outside normal bounds:\n{}".format(self.habTitle, self.habTemp))
        if self.habAlert == 2:
            popup("Feeding alert!\nThe {} is experiencing supply issues:\n{}".format(self.habTitle,self.habFood))
        if self.habAlert == 3:
            popup("Cleanliness alert!\nThe {} has the following sanitary problems:\n{}".format(self.habTitle, self.habClean))

    def __init__(self, sqlid, species, habitat, temperature, feeding, cleaning, alarm):
        self.habID = int(sqlid)
        self.habType = species
        self.habTitle = habitat
        self.habTemp = temperature
        self.habFood = feeding
        self.habClean = cleaning
        self.habAlert = int(alarm)
        