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

#Creating a Window
window = tk.Tk()
window.title("My First Todo App")
window.geometry("600x400")

#Label 1
welcome_label = tk.Label(window, text="Welcome to my To-Do App!", font=("Arial", 20))
welcome_label.pack(pady=20)

#Button 1
test_button = tk.Button(window, text="Click Me!", bg="lightblue", font=("Arial", 12))
test_button.pack(pady=10)

#Instructions?
instruct_label = tk.Label(window, text="Instruction: Click the Button Pls", font=("Arial", 12))
instruct_label.pack(pady=5)

#Window Open
window.mainloop()