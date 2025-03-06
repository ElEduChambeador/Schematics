import pandas as pd
import os

#####################################################################################################
# Flag to be Capacitors or Resistors
C_OR_R = 'R'
#####################################################################################################

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

def main():
    # User input
    if 'R' == C_OR_R:
        excel_file = "Resistors.xlsx"
    elif 'C' == C_OR_R:
        excel_file = "Capacitors.xlsx"
    
    # Read the Excel file
    df = read_excel(excel_file)

    # Open log file for writing
    log_file_path = "insertion_log.txt"
    with open(log_file_path, 'w') as log_file:
        # Process each row in the Excel file
        for _, row in df.iterrows():
            value = row['Value']
            if 'R' == C_OR_R:
                lbr_file_path = os.path.join('Resistor', f"{value}.lbr")
            elif 'C' == C_OR_R:
                lbr_file_path = os.path.join('Capacitor', f"{value}.lbr")
            
            if os.path.exists(lbr_file_path):
                device_set = generate_device_set(row, C_OR_R)
                insert_device_set(lbr_file_path, device_set)
                log_file.write(f"Inserted device set for {row['Part Number']} into {lbr_file_path}\n")
                print(f"Inserted device set for {row['Part Number']} into {lbr_file_path}")
            else:
                log_file.write(f"Warning: {lbr_file_path} does not exist. Skipping.\n")
                print(f"Warning: {lbr_file_path} does not exist. Skipping.")

    print("Device sets have been added to the respective .lbr files. Log has been created.")

if __name__ == "__main__":
    main()

