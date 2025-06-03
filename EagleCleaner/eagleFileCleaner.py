import os
import tkinter as tk
from tkinter import filedialog

# Create a Tkinter root window (it won't be shown)
root = tk.Tk()
root.withdraw()  # Hide the root window

# Open a folder selection dialog
print("Please select the folder containing the .sch and .brd files to process.")
folder_path = filedialog.askdirectory(title="Select Folder Containing .sch and .brd Files")

# Define the lines to be deleted
lines_to_delete = [
    'mouser_part_number',
    'mouser_testing_part_number',
    'mouser_price-stock',
    'arrow_price-stock',
    'arrow_part_number',
    'snapeda_link',
    'purchase-url',
    'check_prices',
    'availability',
    'price',
    'digikey_part_number',
    'digikey_price_stock'
]

# Initialize a log list to store deletion details
deletion_log = []

# Check if a folder was selected
if not folder_path:
    print("No folder selected. Exiting script.")
else:
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist. Please provide a valid folder path.")
    else:
        # Walk through the directory tree
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                # Process only .sch and .brd files
                if filename.lower().endswith(('.sch', '.brd')):
                    file_path = os.path.join(root, filename)
                    
                    # Check if it is a file
                    if os.path.isfile(file_path):
                        # Read the file content
                        with open(file_path, 'r', encoding='utf-8') as file:
                            try:
                                lines = file.readlines()
                            except UnicodeDecodeError:
                                print(f"Could not read {filename} due to encoding issues. Skipping.")
                                continue
                        
                        # Write back the content excluding the lines to be deleted
                        with open(file_path, 'w', encoding='utf-8') as file:
                            for line in lines:
                                if not any(delete_line in line.lower() for delete_line in lines_to_delete):
                                    file.write(line)
                                else:
                                    deletion_log.append(f"Deleted from {os.path.join(root, filename)}: {line.strip()}")

        # Write the deletion log to a .txt file in the selected folder
        log_file_path = os.path.join(folder_path, 'deletion_log.txt')
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            for log_entry in deletion_log:
                log_file.write(log_entry + '\n')

        print(f"Processing complete. Lines containing specified strings have been deleted from all .sch and .brd files in the folder and its subfolders.")
        print(f"A log of deletions has been saved to '{log_file_path}'.")