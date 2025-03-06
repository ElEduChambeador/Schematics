import re

def extract_pin_names(data):
    """
    Extracts pin names from the given data.
    
    Args:
    - data (str): The string containing the pin definitions.
    
    Returns:
    - list: A list of extracted pin names in order.
    """
    pattern = r"Pin '([^']+)'"
    pin_names = re.findall(pattern, data)
    return pin_names

def replace_pin_names(pin_names, replacements):
    """
    Replaces sequences in the pin names based on the replacements dictionary,
    removing any numbers after the underscore and handling case insensitivity.
    
    Args:
    - pin_names (list): List of pin names.
    - replacements (dict): Dictionary of replacement rules (e.g., {'VDD1_': 'VDD1'}).
    
    Returns:
    - list: A list of pin names after applying the replacements.
    """
    updated_pins = []
    for pin in pin_names:
        original_pin = pin
        for key, value in replacements.items():
            # Handle case insensitivity and remove underscores and numbers after the prefix
            if re.search(rf"^{key}", pin, re.IGNORECASE):
                pin = re.sub(rf"^{re.escape(key)}\d*", value, pin, flags=re.IGNORECASE)
        updated_pins.append(pin)
    return updated_pins

def remove_extra_suffixes(pin_names):
    """
    Removes any numeric suffixes (e.g., '_2', '_3', etc.) from the pin names.
    
    Args:
    - pin_names (list): List of pin names.
    
    Returns:
    - list: A list of pin names with numeric suffixes removed.
    """
    return [re.sub(r"(_\d+)$", "", pin) for pin in pin_names]

def filter_exceptions(pin_names, exceptions):
    """
    Filters out pins that are in the exceptions list.
    
    Args:
    - pin_names (list): List of cleaned pin names.
    - exceptions (list): List of pin names to be excluded from the final list.
    
    Returns:
    - list: A list of pin names after filtering out the exceptions.
    """
    return [pin for pin in pin_names if pin not in exceptions]

# Input data: Replace 'YOUR_TEXT_HERE' with your input string
data = """
Pin 'SCL/CCLK(I2S/!LJ)' In None Long R0 Both 0 (0 0)
Pin 'ADO/!CS(DEM)' In None Long R0 Both 0 (0 -100)
Pin 'VA_HP' Pwr None Long R0 Both 0 (0 -200)
Pin 'FLYP' In None Long R0 Both 0 (0 -300)
Pin 'GND_HP' Pwr None Long R0 Both 0 (0 -400)
Pin 'FLYN' In None Long R0 Both 0 (0 -500)
Pin 'VA' Pwr None Long R0 Both 0 (0 -600)
Pin 'AGND' Pwr None Long R0 Both 0 (0 -700)
Pin 'MICIN1/AIN3A' In None Long R0 Both 0 (0 -800)
Pin 'AIN2A' In None Long R0 Both 0 (0 -900)
Pin 'AIN1A' In None Long R0 Both 0 (0 -1000)
Pin 'AIN1B' In None Long R0 Both 0 (0 -1100)
Pin '!RESET' In None Long R0 Both 0 (0 -1200)
Pin 'MCLK' In None Long R0 Both 0 (0 -1300)
Pin 'SDIN' In None Long R0 Both 0 (0 -1400)
Pin 'LRCK' I/O None Long R180 Both 0 (4600 -1700)
Pin 'SDA/CDIN(MCLKDIV2)' I/O None Long R180 Both 0 (4600 -1600)
Pin 'VSS_HP' Out None Long R180 Both 0 (4600 -1500)
Pin 'AOUTB' Out None Long R180 Both 0 (4600 -1400)
Pin 'AOUTA' Out None Long R180 Both 0 (4600 -1300)
Pin 'DAC_FILT+' Out None Long R180 Both 0 (4600 -1200)
Pin 'VQ' Out None Long R180 Both 0 (4600 -1100)
Pin 'ADC_FILT+' Out None Long R180 Both 0 (4600 -1000)
Pin 'MICIN2/BIAS/AIN3B' I/O None Long R180 Both 0 (4600 -900)
Pin 'AIN2B/BIAS' I/O None Long R180 Both 0 (4600 -800)
Pin 'AFILTA' Out None Long R180 Both 0 (4600 -700)
Pin 'AFILTB' Out None Long R180 Both 0 (4600 -600)
Pin 'VL' Pwr None Long R180 Both 0 (4600 -500)
Pin 'VD' Pwr None Long R180 Both 0 (4600 -400)
Pin 'DGND' Pwr None Long R180 Both 0 (4600 -300)
Pin 'SDOUT(M/!S)' I/O None Long R180 Both 0 (4600 -200)
Pin 'SCLK' I/O None Long R180 Both 0 (4600 -100)
Pin '33' Pas None Long R180 Both 0 (4600 0)
"""

# Define replacements
replacements = {
    "VDD1_": "VDD1",
    "VDD1": "VDD1",
    "VDDQ_": "VDD2",
    "VDDQ": "VDD2",
    "VSS_": "GND",
    "VSS": "GND",
    "VDD2_": "VDD2",
    "VDD2": "VDD2",
    "GND_": "GND"
}

# Define exceptions list
exceptions = ["DNU", "NC", "ZQ0", "ZQ1", "RESET_N","P0"]

# Extract, replace, and remove suffixes
pin_names = extract_pin_names(data)
updated_pins = replace_pin_names(pin_names, replacements)
cleaned_pins = remove_extra_suffixes(updated_pins)

# Filter out exceptions
filtered_pins = filter_exceptions(cleaned_pins, exceptions)

# Display results
print("Original Pins:")
print(pin_names)
print("\nUpdated Pins:")
print(updated_pins)
print("\nCleaned Pins:")
print(cleaned_pins)
print("\nFiltered Pins (No Exceptions):")
print(filtered_pins)
