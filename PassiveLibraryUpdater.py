import pandas as pd
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import re

## To use this script, use a local copy of the Library_Passives_Template.xlsx, located at C:\Users\%USERNAME%\Avnet\AVAIL 5.0 - A5 - Design Library\EAGLE Shared Libraries
## Format Example:
##  |Part Number        |Device     |Value  |Unit   |Package Number |Description                                                        |MF     |Lifecycle  |Status |
##  |RC1206FR-0710RL    |Resistor   |10R    |ohms   |1206           |SMD Chip Resistor, 10 Ohm, ± 1%, 250 mW, 1206 [3216 Metric]        |YAGEO  |GREEN      |Done   |
##  |C0603C471K5RACPUTO |Capacitor  |470pF  |pF     |0603           |Ceramic Capacitor, 470 pF, 50 V, ± 10%, X7R, 0603 [1608 Metric]    |KEMET  |GREEN      |Done   |

# Note: Use the correct Value attributes, such as "10R", "10k", "100pF", "0.47pF"; don't use shit like "10", "200r", "13K", "10pf", "47NF". This script is not pendehou-proof

def select_excel_file():
    """Use the Library_Passives_Template.xlsx file if available, otherwise open a file dialog to select an Excel file."""
    default_file = "Library_Passives_Template.xlsx"
    if os.path.exists(default_file):
        return default_file
    
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")]) or "Library_Passives_Template.xlsx"
    return file_path

def read_excel(file_path):
    """Read the Excel file and return the data as a pandas DataFrame."""
    return pd.read_excel(file_path, dtype=str)

def generate_device_set(row, prefix):
    """Generate the XML device set text based on the Excel row and prefix (R or C)."""
    part_number = row['Part Number']
    description = row['Description']
    package_number = row['Package Number']
    manufacturer_name = row['MF']
    value = row['Value']

    # Determine the symbols and other replacements based on prefix
    if prefix == 'R':
        symbol = "R-EU"
        package_prefix = 'R'
    else:
        symbol = "C-EU"
        package_prefix = 'C'

    # Replace placeholders with actual data
    device_set = f"""
<deviceset name="{part_number}" prefix="{prefix}" uservalue="yes">
    <description>{description}</description>
    <gates>
        <gate name="G$1" symbol="{symbol}" x="0" y="0"/>
    </gates>
    <devices>
        <device name="" package="{package_prefix}{package_number}">
            <connects>
                <connect gate="G$1" pin="1" pad="1"/>
                <connect gate="G$1" pin="2" pad="2"/>
            </connects>
            <technologies>
                <technology name="">
                    <attribute name="MANUFACTURER_NAME" value="{manufacturer_name}" constant="no"/>
                    <attribute name="MANUFACTURER_PART_NUMBER" value="{part_number}" constant="no"/>
                    <attribute name="SPICEPREFIX" value="{prefix}" constant="no"/>
                    <attribute name="VALUE" value="{value}" constant="no"/>
                </technology>
            </technologies>
        </device>
    </devices>
    <spice>
        <pinmapping spiceprefix="{prefix}">
            <pinmap gate="G$1" pin="1" pinorder="1"/>
            <pinmap gate="G$1" pin="2" pinorder="2"/>
        </pinmapping>
    </spice>
</deviceset>
    """
    return device_set.strip()

def insert_device_set(lbr_file_path, device_set):
    """Open the .lbr file, insert the device set, and save the modified file."""
    with open(lbr_file_path, 'r') as file:
        lines = file.readlines()

    # Find the first occurrence of <devicesets> and insert the device set after it
    for i, line in enumerate(lines):
        if "<devicesets>" in line:
            lines.insert(i + 1, device_set + "\n")
            break
    
    # Save the modified file
    with open(lbr_file_path, 'w') as file:
        file.writelines(lines)

def device_exists(lbr_file_path, part_number):
    with open(lbr_file_path, 'r') as file:
        return any(f'<deviceset name="{part_number}"' in line for line in file)
    
def package_exists(lbr_file_path, package):
    with open(lbr_file_path, 'r') as file:
        return any(f'<package name="{package}"' in line for line in file)
    
def is_valid_value(value):
    #print(value)
    """Check if the value contains a unit (e.g., k, R, pF, nF, etc.)."""
    return bool(re.search(r'[a-zA-Z]', value))

def is_valid_part_number(part_number):
    return " " not in part_number

def main():
    # Select Excel file through GUI
    excel_file = select_excel_file()
    if not excel_file:
        print("No file selected. Exiting.")
        return
    
    # Read the Excel file
    df = read_excel(excel_file)
    
    # Process missing .lbr files
    source_folder = 'TemplateLib'
    os.makedirs('Resistor', exist_ok=True)
    os.makedirs('Capacitor', exist_ok=True)
    
    log_file_path = "insertion_log.txt"
    with open(log_file_path, 'w') as log_file:
        for _, row in df.iterrows():
            if row['Status'] == 'Done' or row['Status'] == 'In Progress':
                continue
            
            part_number = row['Part Number']
            package = row['Package Number']
            device_type = row['Device']
            value = row['Value']
            
            if not is_valid_part_number(part_number):
                log_file.write(f"Warning: Invalid part number '{part_number}'. Skipping.\n")
                df.at[_, 'Status'] = 'Review Part Number'
                continue
            
            if not is_valid_value(value):
                log_file.write(f"Warning: Invalid value '{value}' for part {row['Part Number']}. Skipping.\n")
                df.at[_, 'Status'] = 'Review Device or Values'
                continue
            
            if device_type == 'Resistor':
                prefix = 'R'
                destination_folder = 'Resistor'
                source_file = 'ResistorTemplate.lbr'
            elif device_type == 'Capacitor':
                prefix = 'C'
                destination_folder = 'Capacitor'
                source_file = 'CapacitorTemplate.lbr'
            else:
                log_file.write(f"Warning: Unknown device type {device_type}. Skipping.\n")
                print(f"Warning: Unknown device type {device_type}. Skipping.")
                df.at[_, 'Status'] = 'Review Device or Values'
                continue
            
            if not is_valid_value(f"{prefix}{package}"):
                log_file.write(f"Warning: Invalid package '{package}' for part {row['Part Number']}. Skipping.\n")
                df.at[_, 'Status'] = 'Review Package'
                continue
            
            lbr_file_path = os.path.join(destination_folder, f"{value}.lbr")
            if not os.path.exists(lbr_file_path):
                shutil.copy(os.path.join(source_folder, source_file), lbr_file_path)
                log_file.write(f"Created new .lbr file: {lbr_file_path}\n")
                print(f"Created new .lbr file: {lbr_file_path}")
        
        # Process each row in the Excel file
        for _, row in df.iterrows():
            if row['Status'] == 'Done' or row['Status'] == 'In Progress':
                continue
            
            part_number = row['Part Number']
            package = row['Package Number']
            device_type = row['Device']
            value = row['Value']
            
            if not is_valid_part_number(part_number):
                log_file.write(f"Warning: Invalid part number '{part_number}'. Skipping.\n")
                print(f"Warning: Invalid part number '{part_number}'. Skipping.")
                df.at[_, 'Status'] = 'Review Part Number'
                continue
            
            if not is_valid_value(value):
                log_file.write(f"Warning: Invalid value '{value}' for part {row['Part Number']}. Skipping.\n")
                print(f"Warning: Invalid value '{value}' for part {row['Part Number']}. Skipping.")
                df.at[_, 'Status'] = 'Review Values'
                continue
            
            if device_type == 'Resistor':
                prefix = 'R'
                lbr_file_path = os.path.join('Resistor', f"{value}.lbr")
            elif device_type == 'Capacitor':
                prefix = 'C'
                lbr_file_path = os.path.join('Capacitor', f"{value}.lbr")
            else:
                log_file.write(f"Warning: Unknown device type {device_type}. Skipping.\n")
                print(f"Warning: Unknown device type {device_type}. Skipping.")
                df.at[_, 'Status'] = 'Review Device'
                continue
            
            if not is_valid_value(f"{prefix}{package}"):
                log_file.write(f"Warning: Invalid package '{package}' for part {row['Part Number']}. Skipping.\n")
                print(f"Warning: Invalid package '{package}' for part {row['Part Number']}. Skipping.")
                df.at[_, 'Status'] = 'Review Package'
                continue
            
            device_set = generate_device_set(row, prefix)
            
            if device_exists(lbr_file_path, row['Part Number']):
                log_file.write(f"Skipping existing device: {row['Part Number']} in {lbr_file_path}\n")
                print(f"Skipping existing device: {row['Part Number']} in {lbr_file_path}")
                df.at[_, 'Status'] = 'Done'
                continue
            
            if not package_exists(lbr_file_path, f"{prefix}{package}"):
                log_file.write(f"Skipping wrong-package device: {row['Part Number']} in {lbr_file_path}\n")
                print(f"Skipping wrong-package device: {row['Part Number']} in {lbr_file_path}")
                df.at[_, 'Status'] = 'Review Package'
                continue
            
            insert_device_set(lbr_file_path, device_set)
            df.at[_, 'Status'] = 'Done'
            log_file.write(f"Inserted device set for {row['Part Number']} into {lbr_file_path}\n")
            print(f"Inserted device set for {row['Part Number']} into {lbr_file_path}")
    
    df.to_excel(excel_file, index=False)
    if os.path.getsize(log_file_path) == 0:
        print("No new devices to add on reference")
    else:
        print("Device sets have been added to the respective .lbr files. Log has been created.")

if __name__ == "__main__":
    main()
