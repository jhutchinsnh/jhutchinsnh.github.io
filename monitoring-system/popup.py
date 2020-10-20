'''
Created on Oct 5, 2020

@author: Jason
'''

import tkinter as tk
from tkinter import ttk

def popup(msg):
    pop = tk.Tk()
    pop.wm_title("Alert!")
    label = ttk.Label(pop, text=msg, font=("Helvetica",16))
    label.pack(side="top", fill="x", pady=10)
    button = ttk.Button(pop, text="OK", command=pop.destroy)
    button.pack()
    pop.mainloop()