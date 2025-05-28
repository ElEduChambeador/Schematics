import os
import tkinter as tk
from tkinter import filedialog

def select_folder():
    """Open a dialog to select a folder."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select Folder")
    root.destroy()
    return folder_path

def replace_eagle_version(content):
    """Replace eagle version 9.7.0 with 9.6.2 in the given content."""
    return content.replace('<eagle version="9.7.0">', '<eagle version="9.6.2">')

def process_folder(folder_path):
    """Process all Eagle files in the folder and its subfolders, performing the replacement."""
    modified_files = []
    skipped_files = []
    
    # Walk through the folder and its subfolders
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith('.sch') or filename.lower().endswith('.brd'):  # Process only Eagle files
                file_path = os.path.join(root, filename)
                try:
                    # Read the file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    # Perform replacement
                    modified_content = replace_eagle_version(content)
                    
                    # Save the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(modified_content)
                    
                    modified_files.append(os.path.relpath(file_path, folder_path))
                except Exception as e:
                    skipped_files.append((os.path.relpath(file_path, folder_path), str(e)))
    
    return modified_files, skipped_files

def main():
    """Main function to select folder and process files."""
    folder_path = select_folder()
    if not folder_path:
        print("No folder selected. Exiting.")
        return
    
    print(f"Processing files in: {folder_path}")
    modified_files, skipped_files = process_folder(folder_path)
    
    # Print results
    if modified_files:
        print("\nSuccessfully modified files:")
        for filename in modified_files:
            print(f"- {filename}")
    else:
        print("\nNo files were modified.")
    
    if skipped_files:
        print("\nSkipped files (due to errors):")
        for filename, error in skipped_files:
            print(f"- {filename}: {error}")
    
    print("\nProcessing complete.")

if __name__ == "__main__":
    main()