#OMSAIRAM

"""
Learning Objectives:
- Learn how to build a desktop app using only python
- Learn how to use tkinter
- Document each step

"""


"""
Template:
- A to-do list that lets people add, remove, and view tasks.
- Should be able to send notifications for tasks that are due today.
- Uses a simple text file to store tasks.
- Uses Python's built-in libraries.
"""

import tkinter as tk
from tkinter import ttk

#List of Tasks
tasks = []

#Triggers when Add Task Button is pressed
def add_task(): 
    task_text = task_entry.get()

    #Checks if task_entry has text
    if task_text.strip(): #If has text
        #Add to the Tasks List
        tasks.append(task_text.strip())

        #Removes the text from the field
        task_entry.delete(0, tk.END)

        #Changes the text in the Result Label
        result_label.config(text=f"Added: '{task_text}' | Total Tasks: {len(tasks)}", fg="green")

    else: #If has no text
        result_label.config(text="Please enter a task first!", fg="red")

#Creating a Window
window = tk.Tk()
window.title("My First Todo App")
window.geometry("600x400")

window.mainloop()