import subprocess
import sys

# Function to install PyInstaller
def install_pyinstaller():
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

# Function to create the executable
def create_executable():
    print("Creating executable...")
    subprocess.check_call(['pyinstaller', '--onefile', 'edit_calendar.py'])

# Function to guide the user
def guide_user():
    print("\nSetup complete. The executable has been created in the 'dist' directory.")
    print("Move 'edit_calendar' to the directory where your HTML files are located.")
    print("Run 'edit_calendar' to edit the calendar dates and push changes to GitHub.")

def main():
    print("Starting setup...")
    install_pyinstaller()
    create_executable()
    guide_user()

if __name__ == "__main__":
    main()
