import os
import pandas as pd
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename

# Function to sanitize folder names
def sanitize_name(name):
    # Replace specified invalid characters with an underscore
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

# Function to copy files based on the design name and ID
def copy_files(excel_path, png_folder):
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Ensure the relevant columns are present
    if "Folder Name" not in df.columns or "id" not in df.columns:
        print("The required columns are not present in the Excel file.")
        return

    # Create the output directory in the PNG folder
    output_folder = os.path.join(png_folder, "Output_Folder")
    os.makedirs(output_folder, exist_ok=True)

    # List to keep track of missing files and original/corrected names
    missing_files = []
    name_mapping = []

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        original_name = row["Folder Name"]
        corrected_name = sanitize_name(original_name)
        file_id = row["id"]

        # Create the design name folder
        design_folder_path = os.path.join(output_folder, corrected_name)
        
        # Ensure the design folder is created
        os.makedirs(design_folder_path, exist_ok=True)

        # Construct the possible PNG filenames
        png_file_name_standard = f"{file_id}.png"
        png_file_name_sch = f"{file_id}_sch.png"
        
        # Check for the existence of the files
        found_file = None
        if os.path.isfile(os.path.join(png_folder, png_file_name_standard)):
            found_file = png_file_name_standard
        elif os.path.isfile(os.path.join(png_folder, png_file_name_sch)):
            found_file = png_file_name_sch

        # If a file is found, copy it; otherwise, log the missing file
        if found_file:
            source_file_path = os.path.join(png_folder, found_file)
            destination_file_path = os.path.join(design_folder_path, corrected_name + ".png")
            
            # Copy the file and handle any errors
            try:
                shutil.copy(source_file_path, destination_file_path)
                print(f"Copied {found_file} to {design_folder_path}")
            except Exception as e:
                print(f"Error copying file {found_file}: {e}")
        else:
            print(f"File for ID {file_id} not found.")
            missing_files.append(file_id)

        # Add original and corrected names to the mapping list
        name_mapping.append((original_name, corrected_name))

    # Write missing file IDs to a text file
    if missing_files:
        with open(os.path.join(output_folder, "missing_files.txt"), "w") as f:
            for file_id in missing_files:
                f.write(f"{file_id}\n")
        print(f"Missing file IDs written to {os.path.join(output_folder, 'missing_files.txt')}")

    # Write the original and corrected names to a CSV file
    mapping_df = pd.DataFrame(name_mapping, columns=["Original Name", "Corrected Name"])
    mapping_df.to_csv(os.path.join(output_folder, "name_mapping.csv"), index=False)
    print(f"Name mapping written to {os.path.join(output_folder, 'name_mapping.csv')}")

# Select the folder containing PNG files
Tk().withdraw()  # Hides the root window
png_folder = askdirectory(title="Select the Folder Containing PNG Files")

# Select the Excel file
excel_path = askopenfilename(title="Select the Excel File", filetypes=[("Excel files", "*.xlsx;*.xls")])

# Run the copy function
copy_files(excel_path, png_folder)
