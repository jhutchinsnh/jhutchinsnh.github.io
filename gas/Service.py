'''
Created on Sep 27, 2020

@author: Jason
'''

number = 0
name = ""
price = -1.0
discount = -1

class Service:
    # Print service details for users
    def showService(self):
        print('''
        Service number: {}
        Service name:   {}
        Price:          {}
        Discount:       {}'''.format(self.number, self.name, self.price, self.discount))

    # Print list version of service contents
    def showServiceList(self):
        print "\t{}\t{}\t{}\t{}".format(self.number, self.name, self.price, self.discount)

    def __init__(self, number, name, price, discount):
        self.number = int(number)
        self.name = name
        self.price = price
        self.discount = discount

