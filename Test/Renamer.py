import os
import tkinter as tk
from tkinter import filedialog

def renamerShit(filePath):
    filesList = os.listdir(filePath)
    count = 0

    for fileName in filesList:
        completePath = os.path.join(filePath, fileName)

        if "(CLEANED)" in fileName:
            newName = fileName.replace("(CLEANED)", "").strip()

            newPath = os.path.join(filePath, newName)

            os.rename(completePath, newPath)
            print(f"Renamed: {fileName} -> {newName}")
            count+=1
    print("Total renames:", count)

root = tk.Tk()
root.withdraw()  

filePath = filedialog.askdirectory(title="Select Folder")

if filePath:
    renamerShit(filePath)
else:
    print("Select a folder please.")
    
root.destroy()
