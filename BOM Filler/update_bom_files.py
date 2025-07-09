import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_original_bom(root):
    return filedialog.askopenfilename(
        parent=root,
        title="Select Original BOM CSV File",
        filetypes=[("CSV files", "*.csv")]
    )

def select_csv_folder(root):
    return filedialog.askdirectory(
        parent=root,
        title="Select Folder Containing CSV BOM Files"
    )

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

def read_csv_with_fallback(file_path):
    encodings = ['utf-8', 'latin1', 'iso-8859-1']
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"Successfully read {file_path} with {encoding} encoding")
            return df
        except UnicodeDecodeError:
            print(f"Failed to read {file_path} with {encoding} encoding")
            continue
        except Exception as e:
            print(f"Error reading {file_path} with {encoding}: {str(e)}")
            return None
    print(f"Could not read {file_path} with any encoding")
    return None

def update_bom_files(original_bom_path, csv_folder_path):
    try:
        # Read the original BOM
        original_bom = read_csv_with_fallback(original_bom_path)
        if original_bom is None:
            messagebox.showerror("Error", f"Could not read original BOM file: {original_bom_path}")
            return
        required_columns = ['Part', 'Value', 'Device', 'Package', 'Description', 'MF']
        if not all(col in original_bom.columns for col in required_columns):
            messagebox.showerror("Error", "Original BOM is missing required columns!")
            return

        # Convert Part column to uppercase
        original_bom['Part'] = original_bom['Part'].str.strip().str.upper()

        # Get all CSV files
        csv_files = get_all_csv_files(csv_folder_path, original_bom_path)
        if not csv_files:
            messagebox.showinfo("Info", "No CSV files found in the selected folder or subfolders!")
            return

        updated_files = []
        for csv_file in csv_files:
            try:
                # Read and validate the CSV file
                csv_bom = read_csv_with_fallback(csv_file)
                if csv_bom is None:
                    print(f"Skipping {csv_file}: Could not read file")
                    continue
                if csv_bom.empty:
                    print(f"Skipping {csv_file}: Empty file")
                    continue
                if 'Part' not in csv_bom.columns:
                    print(f"Skipping {csv_file}: Missing 'Part' column")
                    continue

                # Remove unnamed columns
                csv_bom = csv_bom.loc[:, ~csv_bom.columns.str.contains('^Unnamed')]

                # Convert Part column to uppercase
                csv_bom['Part'] = csv_bom['Part'].str.strip().str.upper()

                # Ensure all required columns exist, filling with empty strings if missing
                for col in ['Value', 'Device', 'Package', 'Description', 'MF']:
                    if col not in csv_bom.columns:
                        csv_bom[col] = ''

                # Update using merge
                columns_to_update = ['Value', 'Device', 'Package', 'Description', 'MF']
                csv_bom = csv_bom.drop(columns=columns_to_update, errors='ignore')
                updated_bom = csv_bom.merge(
                    original_bom[['Part', 'Value', 'Device', 'Package', 'Description', 'MF']],
                    on='Part',
                    how='left'
                )

                # Fill NaN values with empty strings for updated columns
                updated_bom[columns_to_update] = updated_bom[columns_to_update].fillna('')

                # Save the updated CSV
                updated_bom.to_csv(csv_file, index=False, encoding='utf-8')
                updated_files.append(csv_file)
                print(f"Updated {csv_file}")

            except Exception as e:
                print(f"Error processing {csv_file}: {str(e)}")

        if updated_files:
            messagebox.showinfo("Success", f"Updated {len(updated_files)} files:\n" + "\n".join(updated_files))
        else:
            messagebox.showinfo("Info", "No files were updated due to errors or missing data.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    root.withdraw()
    try:
        original_bom_path = select_original_bom(root)
        if not original_bom_path:
            messagebox.showerror("Error", "No original BOM file selected!")
            return

        csv_folder_path = select_csv_folder(root)
        if not csv_folder_path:
            messagebox.showerror("Error", "No folder selected!")
            return

        update_bom_files(original_bom_path, csv_folder_path)
    finally:
        root.destroy()

if __name__ == "__main__":
    main()