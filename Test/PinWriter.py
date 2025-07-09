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
import sys
import threading
import os

def get_next_pin_number(current_pin, multiplier):
    return current_pin + 1 * multiplier

def backspace_handler(pin_name, initial_pin, multiplier, tsequence_or_flist, pin_list, stop_event):
    current_pin = initial_pin
    current_index = pin_list.index(current_pin) if current_pin in pin_list else 0

    while not stop_event.is_set():
        keyboard.wait('backspace')
        if tsequence_or_flist:  # Sequence mode
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
            current_index = current_index + 1 if current_index + 1 < len(pin_list) else 0

def delete_handler(stop_event):
    keyboard.wait('delete')
    print("Delete key pressed. Exiting program.")
    stop_event.set()  # Signal all threads to stop
    os._exit(0)  # Forcefully exit the entire program

def main():
    pin_name = "P7_"
    initial_pin = 0
    multiplier = 1
    tsequence_or_flist = False  # Change to True for sequence, False for list
    pin_list = ['PINS']

    print("Waiting to detect backspace... (Press Delete to exit)")

    # Create a stop event to signal threads to exit
    stop_event = threading.Event()

    # Create threads for handling Backspace and Delete keys
    backspace_thread = threading.Thread(target=backspace_handler, 
                                      args=(pin_name, initial_pin, multiplier, tsequence_or_flist, pin_list, stop_event),
                                      daemon=True)
    delete_thread = threading.Thread(target=delete_handler, 
                                   args=(stop_event,),
                                   daemon=True)

    # Start the threads
    backspace_thread.start()
    delete_thread.start()

    # Keep the main thread running
    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted.")
        stop_event.set()
        os._exit(0)

if __name__ == "__main__":
    main()