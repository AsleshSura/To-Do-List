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
window.title("My To-Do App")
window.geometry("600x400")
window.configure(bg="white")


title_label = tk.Label(window, text="My To-Do List", font=("Arial", 12), bg="white")
title_label.pack(pady=20)

#Input Frame
input_frame = tk.Frame(window, bg="white")
input_frame.pack(pady=20)

#Input Box for new tasks
tk.Label(input_frame, text="Enter new task:", font=("Arial", 12), bg="white").pack()
task_entry = tk.Entry(input_frame, font=("Arial", 12), width=20, relief="solid", bd=1)
task_entry.pack(pady=10)

#Buttons Frame
button_frame = tk.Frame(window, bg="white")
button_frame.pack(pady=10)

#Add Task Button Core
add_button = tk.Button(button_frame, text="Add Tasks", command=add_task, bg="lightgreen", font=("Arial", 12), width=12)
add_button.pack(side=tk.LEFT, padx=5)

#Show All Task Button
show_all_button = tk.Button(button_frame, text="Show All Tasks", command=show_all_tasks, bg="lightblue", font=("Arial", 12), width=12)
show_all_button.pack(side=tk.LEFT, padx=5)

#Result Label
result_label = tk.Label(window, text="No tasks yet - add one above!", font=("Arial", 12), bg="white", fg="gray")
result_label.pack(pady=20)

#Instructions?
instructions = tk.Label(window, text="To add a new task: Type a task and click 'Add Task'\nTo see all your tasks: Click 'Show All Tasks'", font=("Arial", 12), bg="white", fg="gray", wraplength=400)
instructions.pack(pady=10)

#Let Enter key add tasks
task_entry.bind("<Return>", lambda event: add_task())


window.mainloop()