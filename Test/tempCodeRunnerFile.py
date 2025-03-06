import re
import tkinter as tk
from tkinter import filedialog

# Function to extract the "Pin" list from the file
def extract_pin_list(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Regex to match the pattern starting from "Pin" and ending at the last "Pin"
    pin_pattern = re.compile(r"(Pin '.*?\(.*\))", re.DOTALL)
    
    # Find all occurrences of the pin list
    pin_lists = pin_pattern.findall(content)

    # Print each pin list separately
    for pin_list in pin_lists:
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
