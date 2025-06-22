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


def update_task_display():
    for widget in task_display_frame.winfo_children():
        widget.destroy()

    if not tasks:
        no_tasks_label = tk.Label(task_display_frame, text="No tasks yet!", font=("Arial", 12), bg="white", fg="gray")
        no_tasks_label.pack(pady=20)
    else:
        for i, task in enumerate(tasks, 1):
            task_frame = tk.Frame(task_display_frame, bg="lightgray", relief="solid", bd=1)
            task_frame.pack(fill="x", padx=5, pady=2)

            task_label = tk.Label(task_frame, text=f"{i}. {task}", font=("Arial", 11), bg="lightgray", anchor="w")
            task_label.pack(side="left", fill="x", expand=True, padx=10, pady=5)

            delete_btn = tk.Button(task_frame, text="Delete", command=lambda idx=i-1: delete_task(idx), bg="red", fg="white", font=("Arial", 9))
            delete_btn.pack(side="right", padx=5, pady=2)


def add_task(): #Adds task to the list "tasks"
    task_text = task_entry.get()

    #Checks if task_entry has text
    if task_text.strip(): 
        #Add to the Tasks List
        tasks.append(task_text.strip())

        #Removes the text from the field
        task_entry.delete(0, tk.END)

        update_task_display()

        #Changes the text in the Result Label
        result_label.config(text=f"Added: '{task_text}' | Total Tasks: {len(tasks)}", fg="green")

    else: #If has no text
        result_label.config(text="Please enter a task first!", fg="red")


def delete_task(index):

    if 0 <= index < len(tasks):
        deleted_task = tasks.pop(index)
        update_task_display()
        result_label.config(text=f"Deleted : '{deleted_task}", fg="orange")

def clear_all_tasks():

    if tasks:
        if messagebox.askyesno("Clear All", "Are you sure you want to delete all tasks?"):
            tasks.clear()
            update_task_display()
            result_label.config(text="All tasks cleared!", fg="blue")
        else:
            result_label.config(text="No tasks to clear!", fg="gray")

#Creating a Window
window = tk.Tk()
window.title("My To-Do App")
window.geometry("600x500")
window.configure(bg="white")


title_label = tk.Label(window, text="My To-Do List", font=("Arial", 24, "bold"), bg="white", fg="darkblue")
title_label.pack(pady=10)

#Input Frame
input_frame = tk.Frame(window, bg="lightblue", relief="raised", bd=2)
input_frame.pack(fill="x", padx=10, pady=5)

#Input Box for new tasks
tk.Label(input_frame, text="Add a new task:", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=5)
task_entry = tk.Entry(input_frame, font=("Arial", 12), width=40, relief="solid", bd=1)
task_entry.pack(pady=5)

#Buttons Frame
button_frame = tk.Frame(input_frame, bg="lightblue")
button_frame.pack(pady=5)

#Add Task Button
add_button = tk.Button(button_frame, text="Add Tasks", command=add_task, bg="lightgreen", font=("Arial", 11), width=12)
add_button.pack(side="left", padx=5)

#Clear Tasks Button
clear_button = tk.Button(button_frame, text="Clear All Tasks", command=clear_all_tasks, bg="red", font=("Arial", 11, "bold"), width=15)
clear_button.pack(side="left", padx=5)

#Result Label
result_label = tk.Label(window, text="Enter a task above and click 'Add Task'", font=("Arial", 10), bg="white", fg="gray")
result_label.pack(pady=5)

#Task display section
display_label = tk.Label(window, text="Your Tasks:", font=("Arial", 14, "bold"), bg="white", fg="darkgreen")
display_label.pack(pady=(10,5))

#Scrollable frame for tasks
canvas = tk.Canvas(window, bg="white", height=200)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=5)
scrollbar.pack(side="right", fill="y", padx=(10,0), pady=5)

task_display_frame = scrollable_frame

instructions = tk.Label(window, text="Type a task and press Enter or click 'Add Task' \nClick 'Delete' next to any task to remove it\nUse 'Clear All' to remove all tasks", font=("Arial", 9), bg="white", fg="gray", justify="left")
instructions.pack(pady=5)

#Let Enter key add tasks
task_entry.bind("<Return>", lambda event: add_task())

update_task_display()

window.mainloop()