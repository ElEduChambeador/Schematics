import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def select_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
    return file_path

def select_folder():
    folder_path = filedialog.askdirectory()
    return folder_path

def sanitize_filename(filename):
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename

def rename_files(folder_path, excel_path):
    log_file = os.path.join(folder_path, "rename_errors_log.txt")
    mapping_file = os.path.join(folder_path, "rename_mapping.xlsx")
    errors = []
    renamed_files = 0
    name_mappings = []
    
    try:
        df = pd.read_excel(excel_path, dtype=str)
        if "Old Name" not in df.columns or "New Name" not in df.columns:
            raise ValueError("Excel file must contain 'Old Name' and 'New Name' columns.")
        
        name_map = {str(old).strip(): str(new).strip() for old, new in zip(df["Old Name"], df["New Name"])}
        
        for filename in os.listdir(folder_path):
            if filename in name_map:  # Direct match
                new_name = name_map[filename]
                sanitized_name = sanitize_filename(new_name)  # Remove invalid characters
                
                if not sanitized_name.lower().endswith(".png"):
                    sanitized_name += ".png"
                
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, sanitized_name)
                
                if os.path.exists(new_path):
                    errors.append(f"Error: {sanitized_name} already exists. Skipping.")
                else:
                    os.rename(old_path, new_path)
                    renamed_files += 1
                    without_extension = sanitized_name.replace(".png", "")
                    name_mappings.append([new_name, without_extension, new_name != without_extension])
            else:
                errors.append(f"Skipping: {filename} (No match found in Excel)")
    
    except Exception as e:
        errors.append(f"Critical Error: {str(e)}")
    
    with open(log_file, "w") as log:
        log.write("\n".join(errors))
    
    if name_mappings:
        mapping_df = pd.DataFrame(name_mappings, columns=["New Name", "Without Special Chars", "Different Name?"])
        mapping_df.to_excel(mapping_file, index=False)
    
    messagebox.showinfo("Process Complete", f"Renaming completed. {renamed_files} files renamed. Check log for details.")

def main():
    root = tk.Tk()
    root.withdraw()
    
    excel_path = select_excel_file()
    if not excel_path:
        messagebox.showerror("Error", "No Excel file selected.")
        return
    
    folder_path = select_folder()
    if not folder_path:
        messagebox.showerror("Error", "No folder selected.")
        return
    
    rename_files(folder_path, excel_path)

if __name__ == "__main__":
    main()
