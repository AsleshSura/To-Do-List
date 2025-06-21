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
from tkinter import messagebox

#List of Tasks
tasks = []

#Triggers when Add Task Button is pressed
def add_task(): #Adds task to the list "tasks"
    task_text = task_entry.get()

    #Checks if task_entry has text
    if task_text.strip(): 
        #Add to the Tasks List
        tasks.append(task_text.strip())

        #Removes the text from the field
        task_entry.delete(0, tk.END)

        #Changes the text in the Result Label
        result_label.config(text=f"Added: '{task_text}' | Total Tasks: {len(tasks)}", fg="green")

    else: #If has no text
        result_label.config(text="Please enter a task first!", fg="red")

#Triggered when Show All Tasks is pressed
def show_all_tasks(): #Shows all tasks in a pop-up
    #Makes sure the list has 1 or more tasks
    if tasks:
        task_list = "\n".join([f"{i+1}. {task}" for i,task in enumerate(tasks)])
        messagebox.showinfo("All Tasks", f"Your Task:\n\n {task_list}")
    else:
        messagebox.showinfo("All Tasks", "You have no tasks yet!")


#Creating a Window
window = tk.Tk()
window.title("My First Todo App")
window.geometry("600x400")




window.mainloop()