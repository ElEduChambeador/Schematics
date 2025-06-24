import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_original_bom():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Original BOM CSV File",
        filetypes=[("CSV files", "*.csv")]
    )
    return file_path

def select_csv_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(
        title="Select Folder Containing CSV BOM Files"
    )
    return folder_path

def get_all_csv_files(folder_path, original_bom_path):
    csv_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.csv'):
                full_path = os.path.join(root, file)
                try:
                    if full_path != original_bom_path and not os.path.samefile(full_path, original_bom_path):
                        csv_files.append(full_path)
                except OSError:
                    continue
    return csv_files

def update_bom_files(original_bom_path, csv_folder_path):
    try:
        # Read the original BOM
        original_bom = pd.read_csv(original_bom_path)
        required_columns = ['Part', 'Value', 'Device', 'Package', 'Description', 'MF']
        if not all(col in original_bom.columns for col in required_columns):
            messagebox.showerror("Error", "Original BOM is missing required columns!")
            return

        # Get all CSV files in the folder and subfolders
        csv_files = get_all_csv_files(csv_folder_path, original_bom_path)
        if not csv_files:
            messagebox.showinfo("Info", "No CSV files found in the selected folder or subfolders!")
            return

        # Process each CSV file
        for csv_file in csv_files:
            try:
                # Read the CSV file
                csv_bom = pd.read_csv(csv_file)
                if not all(col in csv_bom.columns for col in required_columns):
                    print(f"Skipping {csv_file}: Missing required columns")
                    continue

                # Remove any "Unnamed" columns from the input CSV
                csv_bom = csv_bom.loc[:, ~csv_bom.columns.str.contains('^Unnamed')]

                # Create a copy to avoid modifying the original dataframe
                updated_bom = csv_bom.copy()

                # Update Description and MF columns based on Part
                for index, row in updated_bom.iterrows():
                    part = row['Part']
                    match = original_bom[original_bom['Part'] == part]
                    if not match.empty:
                        updated_bom.at[index, 'Description'] = match.iloc[0]['Description']
                        updated_bom.at[index, 'MF'] = match.iloc[0]['MF']

                # Save the updated CSV without the index
                updated_bom.to_csv(csv_file, index=False)
                print(f"Updated {csv_file}")

            except Exception as e:
                print(f"Error processing {csv_file}: {str(e)}")

        messagebox.showinfo("Success", "All CSV files have been updated successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    original_bom_path = select_original_bom()
    if not original_bom_path:
        messagebox.showerror("Error", "No original BOM file selected!")
        return

    csv_folder_path = select_csv_folder()
    if not csv_folder_path:
        messagebox.showerror("Error", "No folder selected!")
        return

    update_bom_files(original_bom_path, csv_folder_path)

if __name__ == "__main__":
    main()