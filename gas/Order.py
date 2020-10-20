'''
Created on Oct 19, 2020

@author: Jason
'''

number = 0
service_number = 0
quantity = 0

class Order:
    # Print service details for users
    def showOrder(self):
        print('''Order details:
        Order number: {}
        Service number: {}
        Quantity: {}
        '''.format(self.number, self.service_number, self.quantity))

    # Print list version of order contents
    def showOrderList(self):
        print "\t{}\t\t{}\t\t{}".format(self.number, self.service_number, self.quantity)

    def __init__(self, number, service_number, quantity):
        self.number = number
        self.service_number = int(service_number)
        self.quantity = int(quantity)
