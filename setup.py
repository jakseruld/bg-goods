import subprocess
import sys
import os

# Function to install PyInstaller
def install_pyinstaller():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

# Function to create the executable
def create_executable():
    subprocess.check_call(['pyinstaller', '--onefile', 'edit_calendar.py'])

# Function to guide the user
def guide_user():
    print("Setup complete. The executable has been created in the 'dist' directory.")
    print("Move 'edit_calendar.exe' to the directory where your HTML files are located.")
    print("Run 'edit_calendar.exe' to edit the calendar dates and push changes to GitHub.")

def main():
    print("Starting setup...")
    install_pyinstaller()
    create_executable()
    guide_user()

if __name__ == "__main__":
    main()
