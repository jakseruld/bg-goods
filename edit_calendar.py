import tkinter as tk
from tkinter import messagebox
import os
import subprocess

# Configurations
USERNAME = "admin"
PASSWORD = "password"

# Function to update the dates
def update_dates():
    date = date_entry.get()
    event = event_entry.get()
    
    if not date or not event:
        messagebox.showerror("Error", "Please fill in both date and event")
        return

    # Read the current shows from the HTML file
    with open('index.html', 'r') as file:
        lines = file.readlines()

    # Find the section where the shows are listed
    start = next(i for i, line in enumerate(lines) if 'const shows = [' in line)
    end = next(i for i, line in enumerate(lines) if '];' in line and i > start)

    # Insert the new show before the closing bracket
    new_show = f"    {{ date: '{date}', event: '{event}' }},\n"
    lines.insert(end, new_show)

    # Write the updated shows back to the HTML file
    with open('index.html', 'w') as file:
        file.writelines(lines)
    
    # Push the changes to GitHub
    push_to_github()

def push_to_github():
    subprocess.run(['git', 'add', 'index.html'])
    subprocess.run(['git', 'commit', '-m', 'Update shows'])
    subprocess.run(['git', 'push', 'origin', 'main'])
    messagebox.showinfo("Success", "Changes pushed to GitHub")

def login():
    if username_entry.get() == USERNAME and password_entry.get() == PASSWORD:
        login_window.destroy()
        open_editor()
    else:
        messagebox.showerror("Error", "Incorrect username or password")

def open_editor():
    editor_window = tk.Tk()
    editor_window.title("Edit Calendar")

    global date_entry, event_entry
    tk.Label(editor_window, text="Date (Month Day, Year):").pack()
    date_entry = tk.Entry(editor_window)
    date_entry.pack()

    tk.Label(editor_window, text="Event:").pack()
    event_entry = tk.Entry(editor_window)
    event_entry.pack()

    tk.Button(editor_window, text="Update", command=update_dates).pack()

    editor_window.mainloop()

# Main login window
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username:").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password:").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=login).pack()

login_window.mainloop()
