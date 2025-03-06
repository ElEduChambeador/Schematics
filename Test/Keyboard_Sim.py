import keyboard
import time

reps = 11103 # 1103 links
delay = 0.5

def kbrd_sequence():
    keyboard.press_and_release('F2')
    time.sleep(0.1)  # Legacy delay
    keyboard.press_and_release('enter')

time.sleep(5)
for _ in range(reps):
    kbrd_sequence()
    time.sleep(delay)
