'''
Created on Sep 27, 2020

@author: Jason
'''

import os
import platform

plat = platform.system()

if plat == "Windows":
    clearstr = "cls"
else:
    clearstr = "clear"

def clear():
    os.system(clearstr)
