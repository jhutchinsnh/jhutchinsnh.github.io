'''
Created on Oct 5, 2020

@author: Jason
'''

from popup import popup

class animalData():
    '''
    classdocs
    '''

    animalSpecies = ""
    animalName = ""
    animalAge = 0
    animalHealth = ""
    animalFeeding = ""
    animalAlert = 0
    animalID = 0
    
    def showAnimal(self):
        print("""Animal - {}
        Species: {}
        Age: {}
        Health concerns: {}
        Feeding schedule: {}
        
        """.format(self.animalName,                   
                   self.animalSpecies.capitalize(), 
                   self.animalAge, 
                   self.animalHealth, 
                   self.animalFeeding))
        return
        
    def checkAlert(self):
        if self.animalAlert == 1:
            popup("Health alert!\n{} is suffering from the following issues:\n{}".format(self.animalName, self.animalHealth))
        if self.animalAlert == 2:
            popup("Feeding alert!\n{}'s schedule has the following issues:\n{}".format(self.animalName, self.animalFeeding))
        return

    def updateAnimal(self):
        self.animalAge = int(input("Enter age: "))
        self.animalHealth = input("Enter health: ")
        self.animalFeeding = input("Enter feeding information: ")
        self.animalAlarm = int(input("Enter alarm (0: None, 1: Health, 2: Feeding): "))

    def __init__(self, sqlid, species, name, age, health, feeding, alarm):
        self.animalID = int(sqlid)
        self.animalSpecies = species
        self.animalName = name
        self.animalAge = int(age)
        self.animalHealth = health
        self.animalFeeding = feeding
        self.animalAlert = int(alarm)
