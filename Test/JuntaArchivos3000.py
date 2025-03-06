import os
import shutil
import tkinter as tk
from tkinter import filedialog

FILE_EXTENSION = ".sch"
FOLDER_NAME = "_All Schematics"

def select_folder():    
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory()
    return folder_selected

def copy_sch_files(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(FILE_EXTENSION):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_folder, file)
                if src_file != dest_file:  # Check to avoid copying to the same file
                    shutil.copy(src_file, dest_folder)
                    print(f"Copied: {src_file}")

if __name__ == "__main__":
    source_folder = select_folder()
    destination_folder = os.path.join(source_folder, FOLDER_NAME)
    copy_sch_files(source_folder, destination_folder)
    print(f"All .sch files have been copied to {destination_folder}")