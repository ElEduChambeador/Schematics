import pyautogui
import keyboard
import time

legacy = 0.1
sleep = 0.3
long = 1
trigger_key = 'Ins'

def change_window():
    pyautogui.hotkey('Alt', 'Tab')
    time.sleep(sleep)
    #pyautogui.press('Enter')
    #time.sleep(legacy)
    
def copy_value():
    #pyautogui.hotkey('Ctrl', 'C')
    keyboard.press('Ctrl')
    time.sleep(legacy)
    keyboard.press_and_release('c')
    time.sleep(sleep)
    keyboard.release('Ctrl')
    time.sleep(legacy)
    pyautogui.press('Tab')
    time.sleep(legacy)
    
def paste_value():
    pyautogui.hotkey('Ctrl', 'V')
    time.sleep(sleep)
    pyautogui.press('Tab')
    time.sleep(legacy)
    
def paste_value_enter_tab():
    pyautogui.hotkey('Ctrl', 'V')
    time.sleep(sleep)
    pyautogui.press('Enter')
    time.sleep(legacy)
    pyautogui.press('Tab')
    time.sleep(legacy)
    
def paste_value_enter():
    pyautogui.hotkey('Ctrl', 'V')
    time.sleep(sleep)
    pyautogui.press('Enter')
    time.sleep(legacy)

def copy_and_paste_excel_to_jira_stage1():
    change_window()
    copy_value()
    change_window()
    paste_value()
    
def copy_and_paste_excel_to_jira_stage2():
    change_window()
    copy_value()
    change_window()
    paste_value_enter_tab()
    
def copy_and_paste_excel_to_jira_stage2_1():
    change_window()
    copy_value()
    change_window()
    paste_value_enter()
    
def main():
    while True:
        #Start on Jira Summary box
        keyboard.wait(trigger_key)
        
        #Copy and paste Summary
        copy_and_paste_excel_to_jira_stage1()
        #Particularities
        pyautogui.press('Tab')
        time.sleep(legacy)
        
        #Copy and paste Description
        copy_and_paste_excel_to_jira_stage1()
        #Copy and paste MFG
        copy_and_paste_excel_to_jira_stage1()
        #Copy and paste Regions
        copy_and_paste_excel_to_jira_stage1()
        #Copy and paste DH URL
        copy_and_paste_excel_to_jira_stage1()
        #Copy and paste DH Code
        copy_and_paste_excel_to_jira_stage1()
        #Copy and paste SVG Name
        copy_and_paste_excel_to_jira_stage1()
        #Copy and paste SVG URL
        copy_and_paste_excel_to_jira_stage1()
        
        pyautogui.press('Tab')
        time.sleep(sleep)
        keyboard.press_and_release('Spacebar')
        time.sleep(sleep)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(sleep)
        keyboard.press_and_release('Spacebar')
        time.sleep(sleep)
        pyautogui.press('Tab')
        time.sleep(legacy)
        
        #Start on Jira Creation Type box
        #keyboard.wait(trigger_key)
        
        #Copy and paste Creation Type
        copy_and_paste_excel_to_jira_stage2()
        
        #Copy and paste Design Stage
        copy_and_paste_excel_to_jira_stage2_1()
        #Particularities
        time.sleep(sleep)
        pyautogui.press('Enter')
        time.sleep(sleep)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(legacy)
        
        #Copy and paste Design Stage
        copy_and_paste_excel_to_jira_stage2()
        #Copy and paste Sprint
        copy_and_paste_excel_to_jira_stage2()
        #Copy and paste Story Point Estimate
        copy_and_paste_excel_to_jira_stage1()
        #Copy and paste Sent Date
        copy_and_paste_excel_to_jira_stage2()
        #Copy and paste Uploaded Date
        copy_and_paste_excel_to_jira_stage2()
        
        
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Tab')
        time.sleep(legacy)
        pyautogui.press('Enter')
        time.sleep(legacy)
        
        change_window()
        pyautogui.press('Y')
        time.sleep(legacy)
        pyautogui.press('Enter')
        
if __name__ == "__main__":
    main()
