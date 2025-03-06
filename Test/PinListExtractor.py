import re
import tkinter as tk
from tkinter import filedialog

# Function to extract the "Pin" list from the file
def extract_pin_list(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Regex to match the "Pin" lines and stop at the first non-Pin line (by looking for lines that don't start with "Pin")
    pin_pattern = re.compile(r"(Pin '.*?\(.*\));", re.DOTALL)
    
    # Find all occurrences of the pin list
    pin_lists = pin_pattern.findall(content)

    # Print the first 3 Pin lists (or less if there are fewer)
    for pin_list in pin_lists[:3]:  # Limit to the first 3 matches
        print(pin_list.strip())
        print("-" * 50)  # Separate each list with a line of dashes

# Function to open a file dialog to select the file
def select_file():
    # Set up tkinter root (hidden window)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog and ask for .scr file
    file_path = filedialog.askopenfilename(
        title="Select your .scr file", 
        filetypes=[("SCR Files", "*.scr"), ("All Files", "*.*")]
    )

    # If a file was selected, process it
    if file_path:
        extract_pin_list(file_path)
    else:
        print("No file selected.")

# Run the file selection and extraction process
select_file()
