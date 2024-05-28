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

    shows.append({"date": date, "event": event})
    refresh_show_list()

def refresh_show_list():
    for widget in show_frame.winfo_children():
        widget.destroy()

    for idx, show in enumerate(shows):
        show_item = tk.Frame(show_frame)
        show_item.pack(fill="x", pady=5)
        
        drag_label = tk.Label(show_item, text="⇅", cursor="fleur")
        drag_label.grid(row=0, column=0)
        drag_label.bind("<ButtonPress-1>", lambda e, idx=idx: on_drag_start(e, idx))
        drag_label.bind("<B1-Motion>", on_drag_motion)
        drag_label.bind("<ButtonRelease-1>", lambda e, idx=idx: on_drag_release(e, idx))

        show_label = tk.Label(show_item, text=f"{show['date']} - {show['event']}", anchor="w")
        show_label.grid(row=0, column=1, sticky="ew")

        remove_button = tk.Button(show_item, text="Remove", command=lambda idx=idx: remove_show(idx))
        remove_button.grid(row=0, column=2)

def remove_show(idx):
    del shows[idx]
    refresh_show_list()

def on_drag_start(event, idx):
    global drag_data
    drag_data = {"idx": idx, "y": event.y_root}

def on_drag_motion(event):
    global drag_data
    delta = event.y_root - drag_data["y"]
    if abs(delta) > 20:
        new_idx = drag_data["idx"] + (1 if delta > 0 else -1)
        if 0 <= new_idx < len(shows):
            shows.insert(new_idx, shows.pop(drag_data["idx"]))
            drag_data["idx"], drag_data["y"] = new_idx, event.y_root
            refresh_show_list()

def on_drag_release(event, idx):
    global drag_data
    drag_data = None

def push_to_github():
    with open('index.html', 'r') as file:
        lines = file.readlines()

    start = next(i for i, line in enumerate(lines) if 'const shows = [' in line)
    end = next(i for i, line in enumerate(lines) if '];' in line and i > start)

    new_shows_content = "".join([f"    {{ date: '{show['date']}', event: '{show['event']}' }},\n" for show in shows])
    lines[start + 1:end] = [new_shows_content]

    with open('index.html', 'w') as file:
        file.writelines(lines)

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
    global date_entry, event_entry, show_frame

    editor_window = tk.Tk()
    editor_window.title("Edit Calendar")

    tk.Label(editor_window, text="Date (Month Day, Year):").pack()
    date_entry = tk.Entry(editor_window)
    date_entry.pack()

    tk.Label(editor_window, text="Event:").pack()
    event_entry = tk.Entry(editor_window)
    event_entry.pack()

    tk.Button(editor_window, text="Add Show", command=update_dates).pack()

    show_frame = tk.Frame(editor_window)
    show_frame.pack(fill="both", expand=True, pady=10)

    tk.Button(editor_window, text="Push to GitHub", command=push_to_github).pack()

    refresh_show_list()
    editor_window.mainloop()

# Main login window
shows = []

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
