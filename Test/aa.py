import os
import tkinter as tk
from tkinter import filedialog

def find_empty_subfolders(folder_path):
    empty_folders = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # Check if the directory is empty
            if not os.listdir(dir_path):
                empty_folders.append(dir_path)
    
    return empty_folders

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    folder_path = filedialog.askdirectory(title="Select a Folder")
    return folder_path

if __name__ == "__main__":
    folder_path = select_folder()
    
    if folder_path:  # Ensure a folder was selected
        empty_subfolders = find_empty_subfolders(folder_path)
        
        if empty_subfolders:
            print("Empty subfolders found:")
            for folder in empty_subfolders:
                print(folder)
        else:
            print("No empty subfolders found.")
    else:
        print("No folder was selected.")

