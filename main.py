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
            file.write(f"{task['text']}||{task['completed']}||{task["timestamp"]}||{task["priority"]}||{due_date}||{category}\n")

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
            task_text = f"{task_time} - {task["text"]}"
            
            if task["priority"]:
                task_text = "★ " + task_text
            if task["completed"]:
                task_text = "✓ " + task_text
            
            if task.get("category") and task.get("category") != "General":
                category_badge = f" [{task.get("category")}]"
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
                    due_text = f"(Due: {date_part} at {time_part})"
                else:
                    due_text += f"Due: {task["due_date"]}"

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
            command=lambda idx=i-1: delete_task(idx), 
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
        if due_date_picker.get() != "":  # Only process date if something is selected
            try:
                date_str = due_date_picker.get_date().strftime('%m-%d-%y')
                
                # Only process time if all time fields are set
                if all(var.get() != "-" for var in [hour_var, min_var, ampm_var]):
                    hour = int(hour_var.get())
                    minute = int(min_var.get())
                    
                    if ampm_var.get() == "PM" and hour != 12:
                        hour += 12
                    elif ampm_var.get() == "AM" and hour == 12:
                        hour = 0
                    due_date = f"{date_str} {hour:02d}:{minute:02d}"
                else:
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
        result_label.configure(text=f"Deleted : '{deleted_task["text"]}'", text_color="orange")

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
        # ...rest of the display logic same as update_task_display...
        date_frame = ctk.CTkFrame(task_display_frame)
        date_frame.pack(fill="x", padx=5, pady=(10,2))
        # ...continue with existing display code...


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
scrollable_frame = ctk.CTkScrollableFrame(window, height=200)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

task_display_frame = scrollable_frame

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

update_task_display()

window.mainloop()
