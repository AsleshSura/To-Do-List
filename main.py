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

import customtkinter as ctk
from tkinter import messagebox

#List of Tasks
tasks = []

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def update_task_display():
    for widget in task_display_frame.winfo_children():
        widget.destroy()

    if not tasks:
        no_tasks_label = ctk.CTkLabel(task_display_frame, text="No tasks yet!", font=("Arial", 12))
        no_tasks_label.pack(pady=20)
    else:
        for i, task in enumerate(tasks, 1):
            task_frame = ctk.CTkFrame(task_display_frame)
            task_frame.pack(fill="x", padx=5, pady=2)

            task_label = ctk.CTkLabel(task_frame, text=f"{i}. {task}", font=("Arial", 11), anchor="w")
            task_label.pack(side="left", fill="x", expand=True, padx=10, pady=5)

            delete_btn = ctk.CTkButton(task_frame, text="Delete", command=lambda idx=i-1: delete_task(idx), fg_color="red", hover_color="darkred", width=70, height=25)
            delete_btn.pack(side="right", padx=5, pady=2)


def add_task(): #Adds task to the list "tasks"
    task_text = task_entry.get()

    #Checks if task_entry has text
    if task_text.strip(): 
        #Add to the Tasks List
        tasks.append(task_text.strip())

        #Removes the text from the field
        task_entry.delete(0, len(task_text))

        update_task_display()

        #Changes the text in the Result Label
        result_label.configure(text=f"Added: '{task_text}' | Total Tasks: {len(tasks)}", text_color="green")

    else: #If has no text
        result_label.configure(text="Please enter a task first!", text_color="red")

def delete_task(index):

    if 0 <= index < len(tasks):
        deleted_task = tasks.pop(index)
        update_task_display()
        result_label.configure(text=f"Deleted : '{deleted_task}'", text_color="orange")

def clear_all_tasks():

    if tasks:
        if messagebox.askyesno("Clear All", "Are you sure you want to delete all tasks?"):
            tasks.clear()
            update_task_display()
            result_label.configure(text="All tasks cleared!", text_color="blue")
    else:
        result_label.configure(text="No tasks to clear!", text_color="gray")

#Creating a Window
window = ctk.CTk()
window.title("My To-Do App")
window.geometry("600x500")

title_label = ctk.CTkLabel(window, text="My To-Do List", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

#Input Frame
input_frame = ctk.CTkFrame(window)
input_frame.pack(fill="x", padx=10, pady=5)

#Input Box for new tasks
ctk.CTkLabel(input_frame, text="Add a new task:", font=("Arial", 12, "bold")).pack(pady=5)
task_entry = ctk.CTkEntry(input_frame, font=("Arial", 12), width=300)
task_entry.pack(pady=5)

#Buttons Frame
button_frame = ctk.CTkFrame(input_frame)
button_frame.pack(pady=5)

#Add Task Button
add_button = ctk.CTkButton(button_frame, text="Add Tasks", command=add_task, fg_color="green", hover_color="darkgreen", width=120)
add_button.pack(side="left", padx=5)

#Clear Tasks Button
clear_button = ctk.CTkButton(button_frame, text="Clear All Tasks", command=clear_all_tasks, fg_color="red", hover_color="darkred", width=120)
clear_button.pack(side="left", padx=5)

#Result Label
result_label = ctk.CTkLabel(window, text="Enter a task above and click 'Add Task'", font=("Arial", 10))
result_label.pack(pady=5)

#Task display section
display_label = ctk.CTkLabel(window, text="Your Tasks:", font=("Arial", 14, "bold"))
display_label.pack(pady=(10,5))

#Scrollable frame for tasks
scrollable_frame = ctk.CTkScrollableFrame(window, height=200)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

task_display_frame = scrollable_frame

instructions = ctk.CTkLabel(window, text="Type a task and press Enter or click 'Add Task' \nClick 'Delete' next to any task to remove it\nUse 'Clear All' to remove all tasks", font=("Arial", 9))
instructions.pack(pady=5)

#Let Enter key add tasks
task_entry.bind("<Return>", lambda event: add_task())

update_task_display()

window.mainloop()
