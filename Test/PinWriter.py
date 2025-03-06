# import pyautogui
# import keyboard
# import time

# def get_next_pin_number(current_pin):
#     return current_pin + 1

# def main():
#     pin_name = "DQ"
#     initial_pin = 8
#     write_number = True
#     current_pin = initial_pin

#     print("Waiting to detect backspace...")

#     while True:
#         keyboard.wait('backspace')

#         if(True == write_number):
#             pin_text = f"{pin_name}{current_pin}"
#             time.sleep(0.2)
#             pyautogui.typewrite(pin_text)
#             pyautogui.press('enter')
#         else:
#             pin_text = f"{pin_name}"
#             time.sleep(0.2)
#             pyautogui.typewrite(pin_text)

#         print(f"PIN{current_pin} registered.")

#         current_pin = get_next_pin_number(current_pin)

#         print("Waiting to detect backspace...")
#         time.sleep(0.5)

# if __name__ == "__main__":
#     main()

import pyautogui
import keyboard
import time

def get_next_pin_number(current_pin, multiplier):
    return current_pin + 1*multiplier

def main():
    pin_name = "P6_"
    initial_pin = 0
    multiplier = 1
    write_number = True
    current_pin = initial_pin
    
    # Flag to toggle between sequence and list mode
    TSEQUENCE_OR_FLIST = True  # Change this to True for sequence, False for list
    
    # List of pin numbers to use in list mode
    pin_list = ['SCL/CCLK(I2S/!LJ)', 'ADO/!CS(DEM)', 'VA_HP', 'FLYP', 'GNDHP', 'FLYN', 'VA', 'AGND', 'MICIN1/AIN3A', 'AIN2A', 'AIN1A', 'AIN1B', '!RESET', 'MCLK', 'SDIN', 'LRCK', 'SDA/CDIN(MCLKDIV2)', 'GNDHP', 'AOUTB', 'AOUTA', 'DAC_FILT+', 'VQ', 'ADC_FILT+', 'MICIN2/BIAS/AIN3B', 'AIN2B/BIAS', 'AFILTA', 'AFILTB', 'VL', 'VD', 'DGND', 'SDOUT(M/!S)', 'SCLK', '33']
    current_index = pin_list.index(current_pin) if current_pin in pin_list else 0

    print("Waiting to detect backspace...")

    while True:
        keyboard.wait('backspace')

        if TSEQUENCE_OR_FLIST:  # Sequence mode
            pin_text = f"{pin_name}{current_pin}"
            time.sleep(0.2)
            pyautogui.typewrite(pin_text)
            pyautogui.press('enter')
            print(f"PIN{current_pin} registered.")
            current_pin = get_next_pin_number(current_pin, multiplier)
        else:  # List mode
            pin_text = f"{pin_list[current_index]}"
            time.sleep(0.2)
            pyautogui.typewrite(pin_text)
            pyautogui.press('enter')
            print(f"PIN{pin_list[current_index]} registered.")
            
            # Move to the next pin in the list
            current_index = current_index + 1 if current_index + 1 < len(pin_list) else 0

        print("Waiting to detect backspace...")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
