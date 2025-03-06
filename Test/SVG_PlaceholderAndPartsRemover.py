import tkinter as tk
from tkinter import filedialog
import re
import os
import sys

PREFIX = "A5_"
VALID_CHARACTERS = set("+-()&/:_,.%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'")
MAX_FILENAME_LENGTH = 25 - len(PREFIX)

def clean_filename(filename):
    filename, extension = os.path.splitext(filename)
    if filename.startswith(PREFIX):
        cleaned_name = ''.join(char for char in filename[len(PREFIX): ] if char in VALID_CHARACTERS)[:MAX_FILENAME_LENGTH]
        return PREFIX + cleaned_name + extension
    else:
        cleaned_name = ''.join(char for char in filename if char in VALID_CHARACTERS)[:MAX_FILENAME_LENGTH]
        return PREFIX + cleaned_name + extension

def svg_cleaner(file_paths):
    for file_path in file_paths:
        original_filename = os.path.basename(file_path)
        directory = os.path.dirname(file_path)
        new_filename = clean_filename(original_filename)
        new_file_path = os.path.join(directory, new_filename)
        os.rename(file_path, new_file_path)

        modified_parts = []
        
        with open(new_file_path, 'r') as f:
            svg_content = f.read()
        
        new_content = re.sub(r'class="v-line">\([^)]*\)', 'class="v-line">', svg_content)
        
        for match in re.finditer(r'class="v-line">\([^)]*\)', svg_content):
            modified_parts.append(match.group())
        
        new_content = re.sub(r'text="\([^)]*\)', 'text="', new_content)
        
        for match in re.finditer(r'text="\([^)]*\)', svg_content):
            modified_parts.append(match.group())
        
        with open(new_file_path, 'w') as f:
            f.write(new_content)
        
        output = "File '{}' processed and saved as '{}' [{} chars + {} .svg]\n".format(original_filename, new_filename, len(new_filename)-len(".svg"), len(".svg"))
        output += "Modified parts in '{}':\n".format(new_filename)
        for part in modified_parts:
            output += part + "\n"
        output += "\n"

        changes_file_path = os.path.join(directory, "ChangesLog.txt")
        with open(changes_file_path, "a") as changes_file:
            changes_file.write(output)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    file_paths = filedialog.askopenfilenames(filetypes=[("SVG Files", "*.svg")], title="SVG Cleaner")
    
    if file_paths:
        svg_cleaner(file_paths)
    else:
        print("No files were selected.")

if __name__ == "__main__":
    main()
