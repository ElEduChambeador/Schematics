import os
import shutil
import pandas as pd

#####################################################################################################
# Flag to be Capacitors or Resistors
C_OR_R = 'R'
#####################################################################################################

# Read the Excel file
if 'R' == C_OR_R:
    excel_file = 'Resistors.xlsx'  # Make sure this file exists in the same directory
    sheet_name = 'ResistorValues'
elif 'C' == C_OR_R:
    excel_file = 'Capacitors.xlsx'  # Make sure this file exists in the same directory
    sheet_name = 'CapacitorValues'
    
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Get the 'Value' column
values = df['Value']

# Define source and destination folders
source_folder = 'TemplateLib'
if 'R' == C_OR_R:
    source_file = 'ResistorTemplate.lbr'
    destination_folder = 'Resistor'
elif 'C' == C_OR_R:
    source_file = 'CapacitorTemplate.lbr'
    destination_folder = 'Capacitor'

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Copy the template file for each value in the 'Value' column if it doesn't already exist
for value in values:
    destination_file = os.path.join(destination_folder, f"{value}.lbr")
    if not os.path.exists(destination_file):
        shutil.copy(os.path.join(source_folder, source_file), destination_file)

print("Files copied successfully.")
