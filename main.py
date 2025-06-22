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
from datetime import datetime
from tkcalendar import DateEntry

# Add after the existing imports
import json

# Add these default preferences
DEFAULT_PREFERENCES = {
    "theme": {
        "background": "dark",
        "button_color": "blue",
        "priority_color": "orange",
        "complete_color": "green",
        "delete_color": "red",
        "edit_color": "blue",
        "accent_color": "orange",
        "text_color": "white",
        "header_color": "red"
    },
    "fonts": {
        "title": ("Arial", 24),
        "header": ("Arial", 12),
        "task": ("Arial", 11),
        "button": ("Arial", 10),
        "label": ("Arial", 10)
    },
    "sizes": {
        "window": "600x600",
        "button_width": 120,
        "entry_width": 300,
        "icon_width": 30,
        "icon_height": 25
    }
}

def load_preferences():
    try:
        with open("preferences.txt", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        save_preferences(DEFAULT_PREFERENCES)
        return DEFAULT_PREFERENCES.copy()

def save_preferences(preferences):
    with open("preferences.txt", "w") as file:
        json.dump(preferences, file, indent=4)

#File TaskList

def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            tasks = []
            for line in file:
                if line.strip():
                    text, completed, timestamp, priority, due_date, category = line.strip().split("||")
                    tasks.append({
                        "text": text, 
                        "completed": completed == "True", 
                        "timestamp": timestamp,
                        "priority": priority == "True",
                        "due_date": due_date if due_date != "None" else None,
                        "category": category if category != "None" else "General"
                        })
            return tasks
    except FileNotFoundError:
        return []

def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            due_date = task.get("due_date", "None")
            category = task.get("category", "General")
            file.write(f"{task['text']}||{task['completed']}||{task['timestamp']}||{task['priority']}||{due_date}||{category}\n")

def load_categories():
    try:
        with open("categories.txt", "r") as file:
            categories = ["General"]
            loaded_cats = [line.strip() for line in file if line.strip()]
            categories.extend([cat for cat in loaded_cats if cat not in categories])
            return categories
    except FileNotFoundError:
        return ["General"]

def save_categories():
    with open("categories.txt", "w") as file:
        for category in categories:
            file.write(f"{category}\n")

#List of Tasks
tasks = load_tasks()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def update_task_display():
    for widget in task_display_frame.winfo_children():
        widget.destroy()

    if not tasks:
        no_tasks_label = ctk.CTkLabel(task_display_frame, text="No tasks yet!", font=("Arial", 12))
        no_tasks_label.pack(pady=20)
        return
    
    #Group tasks by date
    tasks_by_date = {}
    for task in tasks:
        date = task["timestamp"].split()[0]
        if date not in tasks_by_date:
            tasks_by_date[date] = []
        tasks_by_date[date].append(task)
    
    for date in sorted(tasks_by_date.keys(), reverse=True):
        # Create date header
        date_frame = ctk.CTkFrame(task_display_frame)
        date_frame.pack(fill="x", padx=5, pady=(10,2))

        date_obj = datetime.now().strptime(date, "%Y-%m-%d")
        date_str = date_obj.strftime("%B %d, %Y")

        date_label = ctk.CTkLabel(date_frame, text=date_str, font=("Arial", 12, "bold"), fg_color="red", corner_radius=6)
        date_label.pack(fill="x", padx=5, pady=5)
        
        date_tasks = tasks_by_date[date]
        date_tasks.sort(key=lambda x: (not x["priority"], x["timestamp"]))

        for i, task in enumerate(tasks_by_date[date], 1):
            task_frame = ctk.CTkFrame(task_display_frame)
            task_frame.pack(fill="x", padx=5, pady=2)

            priority_btn = ctk.CTkButton(
                task_frame,
                text="★" if task["priority"] else "☆",
                command=lambda idx=tasks.index(task): toggle_priority(idx),
                fg_color="orange" if task["priority"] else "gray",
                hover_color="darkorange" if task["priority"] else "gray",
                width=30,
                height=25
            )
            priority_btn.pack(side="left", padx=2)

            complete_btn = ctk.CTkButton(
                task_frame, 
                text="✓" if task["completed"] else "o", 
                command=lambda idx=tasks.index(task): toggle_completed(idx), 
                fg_color="green" if task["completed"] else "gray", 
                hover_color="darkgreen" if task["completed"] else "darkgray", 
                width=30, 
                height=25)
            complete_btn.pack(side="left", padx=5)

            task_time = task["timestamp"].split()[1]
            task_text = f"{task_time} - {task['text']}"
            if task["priority"]:
                task_text = "★ " + task_text
            if task["completed"]:
                task_text = "✓ " + task_text
            
            if task.get("category") and task.get("category") != "General":
                category_badge = f" [{task.get('category')}]"
                task_text += category_badge

            task_label = ctk.CTkLabel(
                task_frame, 
                text=task_text, 
                font=("Arial", 11), 
                anchor="w", 
                text_color="orange" if task["priority"] else ("gray" if task["completed"] else "white"))
            task_label.pack(side="left", fill="x", expand=True, padx=10, pady=5)

            #Due Date
            due_text = ""
            if task.get("due_date"):
                if " " in task["due_date"]:
                    date_part, time_part = task["due_date"].split()
                    # Check if it's today's date
                    today = datetime.now().strftime('%m-%d-%y')
                    if date_part == today:
                        due_text = f"(Due: Today at {time_part})"
                    else:
                        due_text = f"(Due: {date_part} at {time_part})"
                else:
                    # Date only
                    today = datetime.now().strftime('%m-%d-%y')
                    if task["due_date"] == today:
                        due_text = "(Due: Today)"
                    else:
                        due_text = f"(Due: {task['due_date']})"

            due_label = ctk.CTkLabel(
                task_frame,
                text= due_text,
                font=("Arial", 11),
                anchor="e",
                text_color="orange" if task["priority"] else ("gray" if task["completed"] else "white"))
            
            due_label.pack(side="left", padx =5, pady=2)

            edit_btn = ctk.CTkButton(
                task_frame,
                text="Edit",
                command=lambda idx=tasks.index(task): edit_task(idx),
                fg_color="blue",
                hover_color="darkblue",
                width=70,
                height=25
            )
            edit_btn.pack(side="right", padx=5, pady=2)

            delete_btn = ctk.CTkButton(
                task_frame,
                text="Delete",
                command=lambda idx=tasks.index(task): delete_task(idx), 
                fg_color="red", 
                hover_color="darkred", 
                width=70, 
                height=25)
            delete_btn.pack(side="right", padx=5, pady=2)

def add_task():
    task_text = task_entry.get()

    #Checks if task_entry has text
    if task_text.strip(): 
        #Add to the Tasks List
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        due_date = None
        
        # Check if date is selected
        has_date = due_date_picker.get() != ""
        # Check if time is selected (all time fields must be set)
        has_time = all(var.get() != "-" for var in [hour_var, min_var, ampm_var])
        
        if has_date or has_time:
            try:
                # If date is provided, use it; otherwise use current date
                if has_date:
                    date_str = due_date_picker.get_date().strftime('%m-%d-%y')
                else:
                    # Use current date when only time is provided
                    date_str = datetime.now().strftime('%m-%d-%y')
                
                # If time is provided, add it to the date
                if has_time:
                    hour = int(hour_var.get())
                    minute = int(min_var.get())
                    
                    if ampm_var.get() == "PM" and hour != 12:
                        hour += 12
                    elif ampm_var.get() == "AM" and hour == 12:
                        hour = 0
                    due_date = f"{date_str} {hour:02d}:{minute:02d}"
                else:
                    # Date only
                    due_date = date_str            
            except (ValueError, AttributeError):
                pass  
            
        new_category = category_var.get()
        task_dict = {
            "text": task_text.strip(),
            "completed": False,
            "timestamp": timestamp,
            "priority": False,
            "due_date": due_date,
        }
        if new_category != "General":
            task_dict["category"] = new_category
        tasks.append(task_dict)

        save_tasks()
        #Removes the text from the field
        task_entry.delete(0, len(task_text))
        due_date_picker.delete(0, "end")
        hour_var.set("-")
        min_var.set("-")
        ampm_var.set("-")

        update_task_display()

        #Changes the text in the Result Label
        result_text = f"Added: '{task_text}'"
        if due_date:
            if has_date and has_time:
                result_text += f" | Due: {due_date}"
            elif has_time:
                result_text += f" | Due: Today at {due_date.split()[1]}"
            else:
                result_text += f" | Due: {due_date}"
        result_text += f" | Total Tasks: {len(tasks)}"

        result_label.configure(text=result_text, text_color="green")

    else: #If has no text
        result_label.configure(text="Please enter a task first!", text_color="red")

def delete_task(index):

    if 0 <= index < len(tasks):
        deleted_task = tasks.pop(index)
        save_tasks()
        update_task_display()
        result_label.configure(text=f"Deleted : '{deleted_task['text']}'", text_color="orange")

def toggle_completed(index):
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = not tasks[index]["completed"]
        save_tasks()
        update_task_display()

def clear_all_tasks():

    if tasks:
        if messagebox.askyesno("Clear All", "Are you sure you want to delete all tasks?"):
            tasks.clear()
            save_tasks()
            update_task_display()
            result_label.configure(text="All tasks cleared!", text_color="blue")
    else:
        result_label.configure(text="No tasks to clear!", text_color="gray")

def toggle_priority(index):
    if 0 <= index < len(tasks):
        tasks[index]["priority"] = not tasks[index]["priority"]
        save_tasks()
        update_task_display()

def edit_task(index):
    if 0 <= index < len(tasks):
        task = tasks[index]
    
    edit_window = ctk.CTkToplevel()
    edit_window.title("Edit Task")
    edit_window.geometry("400x250")
    edit_window.transient(window)

    edit_entry = ctk.CTkEntry(edit_window, font=("Arial", 12), width = 300)
    edit_entry.insert(0, task["text"])
    edit_entry.pack(pady=20)

    category_frame = ctk.CTkFrame(edit_window)
    category_frame.pack(pady=5)

    edit_category_var = ctk.StringVar(value=task.get("category", "General"))
    category_menu = ctk.CTkOptionMenu(
        category_frame,
        values=categories,
        variable=edit_category_var,
        width=120
    )
    category_menu.pack(side="left", padx=5)

    due_time_frame = ctk.CTkFrame(edit_window)
    due_time_frame.pack(pady=10)

    hour_var = ctk.StringVar(value="12")
    hour_menu = ctk.CTkOptionMenu(
        due_time_frame,
        values=[f"{i:02d}" for i in range(1,13)],
        variable=hour_var,
        width=60
    )
    hour_menu.pack(side="left", padx=5)

    min_var = ctk.StringVar(value="00")
    min_menu = ctk.CTkOptionMenu(
        due_time_frame,
        values=[f"{i:02d}" for i in range(0,60,5)],
        variable=min_var,
        width=60
    )
    min_menu.pack(side="left", padx=5)

    ampm_var = ctk.StringVar(value="PM")
    ampm_menu = ctk.CTkOptionMenu(
        due_time_frame,
        values=["AM", "PM"],
        variable=ampm_var,
        width=60
    )
    ampm_menu.pack(side="left", padx=5)

    def save_edit():
        new_text = edit_entry.get().strip()
        if new_text:
            task["text"] = new_text
            new_category = edit_category_var.get()

            if new_category == "General":
                task.pop("category", None)
            else:
                task["category"] = new_category

            if task.get("due_date"):
                date_part = task["due_date"].split()[0]
                hour = int(hour_var.get())
                minute = int(min_var.get())

                if ampm_var.get() == "PM" and hour != 12:
                    hour += 12
                elif ampm_var.get() == "AM" and hour == 12:
                    hour = 0
                task["due_date"] = f"{date_part} {hour:02d}:{minute:02d}"
            
            save_tasks()
            update_task_display()
            edit_window.destroy()
            result_label.configure(text=f"Task edited successfully!", text_color="green")
    
    

    save_btn = ctk.CTkButton(
        edit_window,
        text="Save",
        command=save_edit,
        fg_color="green",
        hover_color="darkgreen"
    )
    save_btn.pack(pady=10)

    edit_entry.bind("<Return>", lambda event: save_edit())
    edit_entry.focus_set()

def add_new_category():
    dialog = ctk.CTkInputDialog(
        text="Enter new category name:",
        title="Add Category"
    )

    new_category = dialog.get_input()

    if new_category and new_category.strip():
        new_category = new_category.strip()
        if new_category not in categories:
            categories.append(new_category)
            category_menu.configure(values=categories)
            category_filter_menu.configure(values=["All"] + categories)
            category_var.set(new_category)
            save_categories()
            result_label.configure(text=f"Added new category: {new_category}", text_color="green")

def remove_category():
    # Don't allow removing "General" category
    removable_categories = [cat for cat in categories if cat != "General"]
    if not removable_categories:
        result_label.configure(text="No custom categories to remove!", text_color="red")
        return

    dialog = ctk.CTkInputDialog(
        text="Select category number to remove:\n" + 
             "\n".join(f"{i+1}. {cat}" for i, cat in enumerate(removable_categories)),
        title="Remove Category"
    )
    
    choice = dialog.get_input()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(removable_categories):
            category_to_remove = removable_categories[idx]
            # Update tasks with this category to "General"
            for task in tasks:
                if task.get("category") == category_to_remove:
                    task.pop("category", None)
            
            categories.remove(category_to_remove)
            category_menu.configure(values=categories)
            category_filter_menu.configure(values=["All"] + categories)
            category_var.set("General")
            save_categories()
            save_tasks()
            update_task_display()
            result_label.configure(text=f"Removed category: {category_to_remove}", text_color="orange")
        else:
            result_label.configure(text="Invalid category number!", text_color="red")
    except (ValueError, TypeError):
        result_label.configure(text="Please enter a valid number!", text_color="red")

def reset_all():
    if messagebox.askyesno("Reset Everything", "Are you sure you want to reset everything?\nThis will delete all tasks and custom categories!"):
        # Clear tasks
        tasks.clear()
        save_tasks()
        
        # Reset categories to default
        categories.clear()
        categories.append("General")
        save_categories()
        
        category_filter_menu.configure(values=["All", "General"])

        # Reset UI elements
        category_menu.configure(values=categories)
        category_var.set("General")
        task_entry.delete(0, "end")
        due_date_picker.delete(0, "end")
        hour_var.set("-")
        min_var.set("-")
        ampm_var.set("-")
        
        update_task_display()
        result_label.configure(text="Everything has been reset!", text_color="blue")

def search_tasks():
    search_text = search_entry.get().lower()
    
    for widget in task_display_frame.winfo_children():
        widget.destroy()

    if not tasks:
        no_tasks_label = ctk.CTkLabel(task_display_frame, text="No tasks found!", font=("Arial", 12))
        no_tasks_label.pack(pady=20)
        return
    
    # Filter tasks based on search text
    filtered_tasks = {}
    for task in tasks:
        if (search_text in task["text"].lower() or 
            (task.get("category") and search_text in task["category"].lower()) or
            (task.get("due_date") and search_text in task["due_date"].lower())):
            
            date = task["timestamp"].split()[0]
            if date not in filtered_tasks:
                filtered_tasks[date] = []
            filtered_tasks[date].append(task)
    
    if not filtered_tasks:
        no_results_label = ctk.CTkLabel(
            task_display_frame, 
            text="No matching tasks found!", 
            font=("Arial", 12)
        )
        no_results_label.pack(pady=20)
        return

    # Display filtered tasks grouped by date
    for date in sorted(filtered_tasks.keys(), reverse=True):
        date_frame = ctk.CTkFrame(task_display_frame)
        date_frame.pack(fill="x", padx=5, pady=(10,2))

        date_obj = datetime.now().strptime(date, "%Y-%m-%d")
        date_str = date_obj.strftime("%B %d, %Y")

        date_label = ctk.CTkLabel(
            date_frame, 
            text=date_str, 
            font=("Arial", 12, "bold"), 
            fg_color="red", 
            corner_radius=6
        )
        date_label.pack(fill="x", padx=5, pady=5)
        
        date_tasks = filtered_tasks[date]
        date_tasks.sort(key=lambda x: (not x["priority"], x["timestamp"]))

        for i, task in enumerate(date_tasks, 1):
            task_frame = ctk.CTkFrame(task_display_frame)
            task_frame.pack(fill="x", padx=5, pady=2)

            # Add priority button
            priority_btn = ctk.CTkButton(
                task_frame,
                text="★" if task["priority"] else "☆",
                command=lambda idx=tasks.index(task): toggle_priority(idx),
                fg_color="orange" if task["priority"] else "gray",
                hover_color="darkorange" if task["priority"] else "gray",
                width=30,
                height=25
            )
            priority_btn.pack(side="left", padx=2)

            # Add complete button
            complete_btn = ctk.CTkButton(
                task_frame, 
                text="✓" if task["completed"] else "o", 
                command=lambda idx=tasks.index(task): toggle_completed(idx), 
                fg_color="green" if task["completed"] else "gray", 
                hover_color="darkgreen" if task["completed"] else "darkgray", 
                width=30, 
                height=25
            )
            complete_btn.pack(side="left", padx=5)

            # Format task text
            task_time = task["timestamp"].split()[1]
            task_text = f"{task_time} - {task['text']}"
            
            if task["priority"]:
                task_text = "★ " + task_text
            if task["completed"]:
                task_text = "✓ " + task_text
            
            if task.get("category") and task.get("category") != "General":
                category_badge = f" [{task.get('category')}]"
                task_text += category_badge

            # Add task label
            task_label = ctk.CTkLabel(
                task_frame, 
                text=task_text, 
                font=("Arial", 11), 
                anchor="w", 
                text_color="orange" if task["priority"] else ("gray" if task["completed"] else "white")
            )
            task_label.pack(side="left", fill="x", expand=True, padx=10, pady=5)

            # Add due date label
            due_text = ""
            if task.get("due_date"):
                if " " in task["due_date"]:
                    date_part, time_part = task["due_date"].split()
                    # Check if it's today's date
                    today = datetime.now().strftime('%m-%d-%y')
                    if date_part == today:
                        due_text = f"(Due: Today at {time_part})"
                    else:
                        due_text = f"(Due: {date_part} at {time_part})"
                else:
                    # Date only
                    today = datetime.now().strftime('%m-%d-%y')
                    if task["due_date"] == today:
                        due_text = "(Due: Today)"
                    else:
                        due_text = f"(Due: {task['due_date']})"

            due_label = ctk.CTkLabel(
                task_frame,
                text=due_text,
                font=("Arial", 11),
                anchor="e",
                text_color="orange" if task["priority"] else ("gray" if task["completed"] else "white")
            )
            due_label.pack(side="left", padx=5, pady=2)

            # Add edit and delete buttons
            edit_btn = ctk.CTkButton(
                task_frame,
                text="Edit",
                command=lambda idx=tasks.index(task): edit_task(idx),
                fg_color="blue",
                hover_color="darkblue",
                width=70,
                height=25
            )
            edit_btn.pack(side="right", padx=5, pady=2)

            delete_btn = ctk.CTkButton(
                task_frame,
                text="Delete",
                command=lambda idx=tasks.index(task): delete_task(idx),
                fg_color="red",
                hover_color="darkred",
                width=70,
                height=25
            )
            delete_btn.pack(side="right", padx=5, pady=2)

# Add before the window creation:

def apply_filters():
    filtered_tasks = tasks.copy()
    
    # Priority filter
    if priority_var.get() == "Priority Only":
        filtered_tasks = [task for task in filtered_tasks if task["priority"]]
    elif priority_var.get() == "Non-Priority":
        filtered_tasks = [task for task in filtered_tasks if not task["priority"]]
    
    # Status filter
    if status_var.get() == "Completed":
        filtered_tasks = [task for task in filtered_tasks if task["completed"]]
    elif status_var.get() == "Pending":
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # Category filter
    if category_filter_var.get() != "All":
        filtered_tasks = [task for task in filtered_tasks if task.get("category", "General") == category_filter_var.get()]
    
    # Update display with filtered tasks
    display_filtered_tasks(filtered_tasks)

def reset_filters():
    priority_var.set("All")
    status_var.set("All")
    category_filter_var.set("All")
    update_task_display()

def display_filtered_tasks(filtered_tasks):
    for widget in task_display_frame.winfo_children():
        widget.destroy()

    if not filtered_tasks:
        no_tasks_label = ctk.CTkLabel(task_display_frame, text="No matching tasks!", font=("Arial", 12))
        no_tasks_label.pack(pady=20)
        return
    
    # Group tasks by date
    tasks_by_date = {}
    for task in filtered_tasks:
        date = task["timestamp"].split()[0]
        if date not in tasks_by_date:
            tasks_by_date[date] = []
        tasks_by_date[date].append(task)
    
    for date in sorted(tasks_by_date.keys(), reverse=True):
        date_frame = ctk.CTkFrame(task_display_frame)
        date_frame.pack(fill="x", padx=5, pady=(10,2))

        date_obj = datetime.now().strptime(date, "%Y-%m-%d")
        date_str = date_obj.strftime("%B %d, %Y")

        date_label = ctk.CTkLabel(
            date_frame, 
            text=date_str, 
            font=("Arial", 12, "bold"), 
            fg_color="red", 
            corner_radius=6
        )
        date_label.pack(fill="x", padx=5, pady=5)
        
        date_tasks = tasks_by_date[date]
        date_tasks.sort(key=lambda x: (not x["priority"], x["timestamp"]))

        for i, task in enumerate(date_tasks, 1):
            task_frame = ctk.CTkFrame(task_display_frame)
            task_frame.pack(fill="x", padx=5, pady=2)

            # Add priority button
            priority_btn = ctk.CTkButton(
                task_frame,
                text="★" if task["priority"] else "☆",
                command=lambda idx=tasks.index(task): toggle_priority(idx),
                fg_color="orange" if task["priority"] else "gray",
                hover_color="darkorange" if task["priority"] else "gray",
                width=30,
                height=25
            )
            priority_btn.pack(side="left", padx=2)

            # Add complete button
            complete_btn = ctk.CTkButton(
                task_frame, 
                text="✓" if task["completed"] else "o", 
                command=lambda idx=tasks.index(task): toggle_completed(idx), 
                fg_color="green" if task["completed"] else "gray", 
                hover_color="darkgreen" if task["completed"] else "darkgray", 
                width=30, 
                height=25
            )
            complete_btn.pack(side="left", padx=5)

            # Format task text
            task_time = task["timestamp"].split()[1]
            task_text = f"{task_time} - {task['text']}"
            
            if task["priority"]:
                task_text = "★ " + task_text
            if task["completed"]:
                task_text = "✓ " + task_text
            
            if task.get("category") and task.get("category") != "General":
                category_badge = f" [{task.get('category')}]"
                task_text += category_badge

            task_label = ctk.CTkLabel(
                task_frame, 
                text=task_text, 
                font=("Arial", 11), 
                anchor="w", 
                text_color="orange" if task["priority"] else ("gray" if task["completed"] else "white")
            )
            task_label.pack(side="left", fill="x", expand=True, padx=10, pady=5)

            # Add due date label
            due_text = ""
            if task.get("due_date"):
                if " " in task["due_date"]:
                    date_part, time_part = task["due_date"].split()
                    # Check if it's today's date
                    today = datetime.now().strftime('%m-%d-%y')
                    if date_part == today:
                        due_text = f"(Due: Today at {time_part})"
                    else:
                        due_text = f"(Due: {date_part} at {time_part})"
                else:
                    # Date only
                    today = datetime.now().strftime('%m-%d-%y')
                    if task["due_date"] == today:
                        due_text = "(Due: Today)"
                    else:
                        due_text = f"(Due: {task['due_date']})"

            due_label = ctk.CTkLabel(
                task_frame,
                text=due_text,
                font=("Arial", 11),
                anchor="e",
                text_color="orange" if task["priority"] else ("gray" if task["completed"] else "white")
            )
            due_label.pack(side="left", padx=5, pady=2)

            # Add buttons
            edit_btn = ctk.CTkButton(
                task_frame,
                text="Edit",
                command=lambda idx=tasks.index(task): edit_task(idx),
                fg_color="blue",
                hover_color="darkblue",
                width=70,
                height=25
            )
            edit_btn.pack(side="right", padx=5, pady=2)

            delete_btn = ctk.CTkButton(
                task_frame,
                text="Delete",
                command=lambda idx=tasks.index(task): delete_task(idx),
                fg_color="red",
                hover_color="darkred",
                width=70,
                height=25
            )
            delete_btn.pack(side="right", padx=5, pady=2)

def open_preferences():
    pref_window = ctk.CTkToplevel()
    pref_window.title("Preferences")
    pref_window.geometry("500x650")
    pref_window.transient(window)

    current_prefs = load_preferences()

    # Create main scrollable frame
    main_scroll = ctk.CTkScrollableFrame(pref_window, height=580)
    main_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    # Title
    title_label = ctk.CTkLabel(main_scroll, text="Application Preferences", 
                              font=("Arial", 18, "bold"))
    title_label.pack(pady=(0, 20))

    # Theme Section
    theme_frame = ctk.CTkFrame(main_scroll)
    theme_frame.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(theme_frame, text="🎨 Appearance", 
                font=("Arial", 14, "bold")).pack(pady=(10, 5))

    theme_var = ctk.StringVar(value=current_prefs["theme"]["background"])
    ctk.CTkLabel(theme_frame, text="Theme Mode:").pack(pady=(5, 0))
    ctk.CTkOptionMenu(
        theme_frame,
        values=["dark", "light", "system"],
        variable=theme_var,
        width=150
    ).pack(pady=(0, 10))

    # Color Customization Section
    colors_frame = ctk.CTkFrame(main_scroll)
    colors_frame.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(colors_frame, text="🎯 Color Scheme", 
                font=("Arial", 14, "bold")).pack(pady=(10, 5))

    color_options = ["blue", "green", "red", "purple", "orange", "teal"]
    
    # Create color variables
    color_vars = {
        "Button Color": ctk.StringVar(value=current_prefs["theme"]["button_color"]),
        "Priority Color": ctk.StringVar(value=current_prefs["theme"]["priority_color"]),
        "Complete Color": ctk.StringVar(value=current_prefs["theme"]["complete_color"]),
        "Delete Color": ctk.StringVar(value=current_prefs["theme"]["delete_color"]),
        "Edit Color": ctk.StringVar(value=current_prefs["theme"]["edit_color"]),
        "Accent Color": ctk.StringVar(value=current_prefs["theme"]["accent_color"])
    }

    # Create color selection grid
    color_grid = ctk.CTkFrame(colors_frame)
    color_grid.pack(pady=10, padx=10, fill="x")

    for i, (label, var) in enumerate(color_vars.items()):
        row = i // 2
        col = i % 2
        
        color_subframe = ctk.CTkFrame(color_grid)
        color_subframe.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(color_subframe, text=label, font=("Arial", 10)).pack(pady=2)
        ctk.CTkOptionMenu(
            color_subframe,
            values=color_options,
            variable=var,
            width=120
        ).pack(pady=(0, 5))

    # Configure grid weights
    for i in range(2):
        color_grid.columnconfigure(i, weight=1)

    # Font Section
    font_frame = ctk.CTkFrame(main_scroll)
    font_frame.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(font_frame, text="📝 Typography", 
                font=("Arial", 14, "bold")).pack(pady=(10, 5))

    font_families = ["Arial", "Helvetica", "Times New Roman", "Courier", "Calibri"]
    font_sizes = ["8", "9", "10", "11", "12", "14", "16", "18", "20", "24"]

    task_font_var = ctk.StringVar(value=current_prefs["fonts"]["task"][0])
    task_size_var = ctk.StringVar(value=str(current_prefs["fonts"]["task"][1]))

    font_grid = ctk.CTkFrame(font_frame)
    font_grid.pack(pady=10, padx=10, fill="x")

    # Font family selection
    font_family_frame = ctk.CTkFrame(font_grid)
    font_family_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    ctk.CTkLabel(font_family_frame, text="Font Family:", font=("Arial", 10)).pack(pady=2)
    ctk.CTkOptionMenu(
        font_family_frame,
        values=font_families,
        variable=task_font_var,
        width=150
    ).pack(pady=(0, 5))

    # Font size selection
    font_size_frame = ctk.CTkFrame(font_grid)
    font_size_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    ctk.CTkLabel(font_size_frame, text="Font Size:", font=("Arial", 10)).pack(pady=2)
    ctk.CTkOptionMenu(
        font_size_frame,
        values=font_sizes,
        variable=task_size_var,
        width=150
    ).pack(pady=(0, 5))

    # Configure font grid weights
    for i in range(2):
        font_grid.columnconfigure(i, weight=1)

    # Layout & Sizing Section
    sizes_frame = ctk.CTkFrame(main_scroll)
    sizes_frame.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(sizes_frame, text="📐 Layout & Sizing", 
                font=("Arial", 14, "bold")).pack(pady=(10, 5))

    window_size_var = ctk.StringVar(value=current_prefs["sizes"]["window"])
    button_width_var = ctk.StringVar(value=str(current_prefs["sizes"]["button_width"]))
    entry_width_var = ctk.StringVar(value=str(current_prefs["sizes"]["entry_width"]))

    sizes_grid = ctk.CTkFrame(sizes_frame)
    sizes_grid.pack(pady=10, padx=10, fill="x")

    size_inputs = [
        ("Window Size", window_size_var, ["600x600", "700x700", "800x600", "800x800", "1000x800", "1200x900"]),
        ("Button Width", button_width_var, ["80", "100", "120", "150", "180"]),
        ("Entry Width", entry_width_var, ["200", "250", "300", "350", "400"])
    ]

    for i, (label, var, values) in enumerate(size_inputs):
        size_subframe = ctk.CTkFrame(sizes_grid)
        size_subframe.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(size_subframe, text=label, font=("Arial", 10)).pack(pady=2)
        ctk.CTkOptionMenu(
            size_subframe,
            values=values,
            variable=var,
            width=150
        ).pack(pady=(0, 5))

    # Configure sizes grid weights
    for i in range(2):
        sizes_grid.columnconfigure(i, weight=1)

    # Preview Section
    preview_frame = ctk.CTkFrame(main_scroll)
    preview_frame.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(preview_frame, text="👁️ Preview", 
                font=("Arial", 14, "bold")).pack(pady=(10, 5))

    preview_text = ctk.CTkLabel(
        preview_frame,
        text="This is how your tasks will look with the selected font and colors.",
        font=(task_font_var.get(), int(task_size_var.get())),
        fg_color="transparent"
    )
    preview_text.pack(pady=10)

    # Update preview when font changes
    def update_preview(*args):
        try:
            preview_text.configure(font=(task_font_var.get(), int(task_size_var.get())))
        except:
            pass

    task_font_var.trace("w", update_preview)
    task_size_var.trace("w", update_preview)

    # Action Buttons Frame (fixed at bottom)
    button_frame = ctk.CTkFrame(pref_window)
    button_frame.pack(fill="x", padx=10, pady=(0, 10))

    def save_preferences_and_apply():
        new_prefs = {
            "theme": {
                "background": theme_var.get(),
                "button_color": color_vars["Button Color"].get(),
                "priority_color": color_vars["Priority Color"].get(),
                "complete_color": color_vars["Complete Color"].get(),
                "delete_color": color_vars["Delete Color"].get(),
                "edit_color": color_vars["Edit Color"].get(),
                "accent_color": color_vars["Accent Color"].get(),
                "text_color": "black" if theme_var.get() == "light" else "white",
                "header_color": "red"
            },
            "fonts": {
                "title": (task_font_var.get(), 24),
                "header": (task_font_var.get(), 14),
                "task": (task_font_var.get(), int(task_size_var.get())),
                "button": (task_font_var.get(), 10),
                "label": (task_font_var.get(), 10)
            },
            "sizes": {
                "window": window_size_var.get(),
                "button_width": int(button_width_var.get()),
                "entry_width": int(entry_width_var.get()),
                "icon_width": 30,
                "icon_height": 25
            }
        }
        save_preferences(new_prefs)
        apply_preferences()
        pref_window.destroy()
        result_label.configure(text="Preferences saved!", text_color="green")

    def reset_to_defaults():
        if messagebox.askyesno("Reset Preferences", "Reset all preferences to default values?"):
            save_preferences(DEFAULT_PREFERENCES)
            apply_preferences()
            pref_window.destroy()
            result_label.configure(text="Preferences reset to defaults!", text_color="blue")

    # Action buttons
    save_btn = ctk.CTkButton(
        button_frame,
        text="💾 Save & Apply",
        command=save_preferences_and_apply,
        fg_color="green",
        hover_color="darkgreen",
        width=150
    )
    save_btn.pack(side="left", padx=10, pady=10)

    reset_btn = ctk.CTkButton(
        button_frame,
        text="🔄 Reset to Defaults",
        command=reset_to_defaults,
        fg_color="orange",
        hover_color="darkorange",
        width=150
    )
    reset_btn.pack(side="left", padx=10, pady=10)

    cancel_btn = ctk.CTkButton(
        button_frame,
        text="❌ Cancel",
        command=pref_window.destroy,
        fg_color="gray",
        hover_color="darkgray",
        width=150
    )
    cancel_btn.pack(side="right", padx=10, pady=10)

def apply_preferences():
    try:
        prefs = load_preferences()
        
        # Apply theme
        ctk.set_appearance_mode(prefs["theme"]["background"])
        
        # Update window size
        window.geometry(prefs["sizes"]["window"])
        
        # Create fonts
        fonts = {
            key: ctk.CTkFont(family=font[0], size=font[1]) 
            for key, font in prefs["fonts"].items()
        }
        
        # Update basic UI elements
        title_label.configure(font=fonts["title"])
        task_label.configure(font=fonts["header"])
        display_label.configure(font=fonts["header"])
        instructions.configure(font=fonts["label"])
        result_label.configure(font=fonts["label"])
        
        # Update buttons
        for btn in [add_button, clear_button, pref_button, reset_button]:
            if btn:
                btn.configure(
                    font=fonts["button"],
                    width=prefs["sizes"]["button_width"]
                )
        
        # Update entries
        task_entry.configure(
            font=fonts["task"],
            width=prefs["sizes"]["entry_width"]
        )
        
        # Update task display
        update_task_display()
        
    except Exception as e:
        print(f"Error applying preferences: {e}")
        save_preferences(DEFAULT_PREFERENCES)

#Creating a Window
window = ctk.CTk()
window.title("My To-Do App")
window.geometry("600x600")

title_label = ctk.CTkLabel(window, text="My To-Do List", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

# Add after title_label.pack():
search_frame = ctk.CTkFrame(window)
search_frame.pack(fill="x", padx=10, pady=5)

search_label = ctk.CTkLabel(search_frame, text="Search:", font=("Arial", 12))
search_label.pack(side="left", padx=5)

search_entry = ctk.CTkEntry(search_frame, font=("Arial", 12), width=200)
search_entry.pack(side="left", padx=5)

search_btn = ctk.CTkButton(
    search_frame,
    text="Search",
    command=search_tasks,
    fg_color="blue",
    hover_color="darkblue",
    width=70
)
search_btn.pack(side="left", padx=5)

clear_search_btn = ctk.CTkButton(
    search_frame,
    text="Clear",
    command=lambda: [search_entry.delete(0, "end"), update_task_display()],
    fg_color="gray",
    hover_color="darkgray",
    width=70
)
clear_search_btn.pack(side="left", padx=5)

# Add after search_frame and before input_frame:

filter_frame = ctk.CTkFrame(window)
filter_frame.pack(fill="x", padx=10, pady=5)

# Filter options
filter_label = ctk.CTkLabel(filter_frame, text="Filters:", font=("Arial", 12))
filter_label.pack(side="left", padx=5)

# Priority filter
priority_var = ctk.StringVar(value="All")
priority_menu = ctk.CTkOptionMenu(
    filter_frame,
    values=["All", "Priority Only", "Non-Priority"],
    variable=priority_var,
    width=120,
    command=lambda _: apply_filters()
)
priority_menu.pack(side="left", padx=5)

# Status filter
status_var = ctk.StringVar(value="All")
status_menu = ctk.CTkOptionMenu(
    filter_frame,
    values=["All", "Completed", "Pending"],
    variable=status_var,
    width=120,
    command=lambda _: apply_filters()
)
status_menu.pack(side="left", padx=5)

# Category filter
category_filter_var = ctk.StringVar(value="All")
category_filter_menu = ctk.CTkOptionMenu(
    filter_frame,
    values=["All"] + load_categories(),
    variable=category_filter_var,
    width=120,
    command=lambda _: apply_filters()
)
category_filter_menu.pack(side="left", padx=5)

# Clear filters button
clear_filters_btn = ctk.CTkButton(
    filter_frame,
    text="Clear Filters",
    command=lambda: reset_filters(),
    fg_color="gray",
    hover_color="darkgray",
    width=100
)
clear_filters_btn.pack(side="left", padx=5)


#Input Frame
input_frame = ctk.CTkFrame(window)
input_frame.pack(fill="x", padx=10, pady=5)

#Input Box for new tasks
task_label = ctk.CTkLabel(input_frame, text="Add a new task:", font=("Arial", 12, "bold"))
task_label.pack(pady=5)

task_entry = ctk.CTkEntry(input_frame, font=("Arial", 12), width=300)
task_entry.pack(pady=5)

due_date_frame = ctk.CTkFrame(input_frame)
due_date_frame.pack(pady=5)

due_date_label = ctk.CTkLabel(due_date_frame, text="(Optional) Due Date:", font=("Arial", 10))
due_date_label.pack(side="left", padx=5)

# Replace the existing due_date_picker with:
due_date_picker = DateEntry(
    due_date_frame,
    width=12,
    background="darkblue",
    foreground="white",
    borderwidth=2,
    font=("Arial", 10),
    date_pattern="mm-dd-yy",
    showweeknumbers=False,
    selectmode='day',
    year=datetime.now().year,
    month=datetime.now().month,
    day=datetime.now().day,
    firstweekday='sunday',
    selectbackground='darkblue',
    selectforeground='white',
    normalbackground='gray20',
    normalforeground='white',
    weekendbackground='gray30',
    weekendforeground='white',
    headersbackground='gray15',
    headersforeground='white'
)
due_date_picker.delete(0,"end")
due_date_picker.pack(side="left", padx=5)

# Add after the due_date_picker.pack():
clear_date_btn = ctk.CTkButton(
    due_date_frame,
    text="×",
    width=25,
    height=25,
    command=lambda: due_date_picker.delete(0, "end"),
    fg_color="gray30",
    hover_color="gray40"
)
clear_date_btn.pack(side="left", padx=(2, 5))

due_time_frame = ctk.CTkFrame(due_date_frame)
due_time_frame.pack(side="left", padx=5)

hour_var = ctk.StringVar(value="-")
hour_menu = ctk.CTkOptionMenu(
    due_time_frame,
    values= ["-"] + [f"{i:02d}" for i in range(1,13)],
    variable=hour_var,
    width=60
)
hour_menu.pack(side="left")

min_var = ctk.StringVar(value="-")
min_menu = ctk.CTkOptionMenu(
    due_time_frame,
    values=["-"] + [f"{i:02d}" for i in range(0,60,5)],
    variable=min_var,
    width=60
)
min_menu.pack(side="left", padx=5)

ampm_var = ctk.StringVar(value="-")
ampm_menu = ctk.CTkOptionMenu(
    due_time_frame,
    values=["-", "AM", "PM"],
    variable=ampm_var,
    width=60
)
ampm_menu.pack(side="left", padx=5)

category_frame = ctk.CTkFrame(input_frame)
category_frame.pack(pady=5)

category_label = ctk.CTkLabel(category_frame, text="Category:", font=("Arial", 10))
category_label.pack(side="left", padx=5)

categories = load_categories()
category_var = ctk.StringVar(value="General")

category_menu = ctk.CTkOptionMenu(
    category_frame,
    values=categories,
    variable=category_var,
    width=120
)
category_menu.pack(side="left", padx=5)

add_category_btn = ctk.CTkButton(
    category_frame,
    text="Add new Category",
    width=30,
    command=add_new_category,
    fg_color="green",
    hover_color="darkgreen"
)
add_category_btn.pack(side="left", padx=5)


remove_category_btn = ctk.CTkButton(
    category_frame,
    text="Remove Category",
    width=30,
    command=remove_category,
    fg_color="red",
    hover_color="darkred"
)
remove_category_btn.pack(side="left", padx=5)

button_frame = ctk.CTkFrame(input_frame)
button_frame.pack(pady=5)

add_button = ctk.CTkButton(button_frame, text="Add Tasks", command=add_task, fg_color="green", hover_color="darkgreen", width=120)
add_button.pack(side="left", padx=5)

clear_button = ctk.CTkButton(button_frame, text="Clear All Tasks", command=clear_all_tasks, fg_color="red", hover_color="darkred", width=120)
clear_button.pack(side="left", padx=5)

pref_button = ctk.CTkButton(
    button_frame, 
    text="Preferences", 
    command=open_preferences, 
    fg_color="teal", 
    hover_color="darkcyan", 
    width=120
)
pref_button.pack(side="left", padx=5)

reset_button = ctk.CTkButton(
    button_frame, 
    text="Reset All", 
    command=reset_all, 
    fg_color="purple", 
    hover_color="darkmagenta", 
    width=120
)
reset_button.pack(side="left", padx=5)

#Result Label
result_label = ctk.CTkLabel(window, text="Enter a task above and click 'Add Task'", font=("Arial", 10))
result_label.pack(pady=5)

#Task display section
display_label = ctk.CTkLabel(window, text="Your Tasks:", font=("Arial", 14, "bold"))
display_label.pack(pady=(10,5))

#Scrollable frame for tasks
task_display_frame = ctk.CTkScrollableFrame(window, height=200)
task_display_frame.pack(fill="both", expand=True, padx=10, pady=5)

instructions = ctk.CTkLabel(
    window, 
    text="Type a task, set due date (optional) and click 'Add Task'\n" +
         "Click '★' to toggle priority, '✓' to mark complete\n" +
         "Click 'Delete' to remove a task, 'Clear All' to remove all tasks\n" +
         "Use the search bar to filter tasks by text, category, or due date",
    font=("Arial", 9)
)
instructions.pack(pady=10)

#Let Enter key add tasks
task_entry.bind("<Return>", lambda event: add_task())
search_entry.bind("<Return>", lambda event: search_tasks())

# Move this code to just before window.mainloop():
update_task_display()

# Initialize preferences last
preferences = load_preferences()
try:
    apply_preferences()
except Exception as e:
    print(f"Error initializing preferences: {e}")
    save_preferences(DEFAULT_PREFERENCES)

window.mainloop()
