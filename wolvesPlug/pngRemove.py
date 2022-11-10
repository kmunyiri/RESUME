# pngRemover.py - removes png from an image in a given folder

import os
import pyautogui
from pathlib import Path
import time

url = "https://express.adobe.com/tools/remove-background"
cwd = Path.cwd()
for filename in os.listdir(cwd / "Players"):
    basename = Path(cwd / "Players" / filename).stem
    # for i in range(len(basename)):
    if ".DS_Store" not in basename:
        print(basename.split())
x = 30
start = 0

for filename in os.listdir(cwd/"Players"):

    player = Path(cwd / "Players" / filename).stem
    if ".DS_Store" not in player:
        print(f"Now converting {player}......")
        pyautogui.doubleClick(430, 475, duration=0.5)  # click Browse files
        time.sleep(3)  # Give it time to load

        pyautogui.click(855, 20, duration=0.5)      # click search box
        pyautogui.write(player)
        pyautogui.click(600, 60, duration=1)      # click folder
        pyautogui.click(490, 155, duration=1)     # click image
        # pyautogui.press("enter")
        pyautogui.click(990, 650, duration=1)    # click open

        time.sleep(3)

        if pyautogui.locateOnScreen("cancel.png"):
            pyautogui.click(855, 20, duration=0.5)  # click search box
            pyautogui.write(player)
            pyautogui.click(600, 60, duration=1)  # click folder
            pyautogui.click(490, 155, duration=1)  # click image
            # pyautogui.press("enter")
            pyautogui.click(990, 650, duration=1)  # click open

        time.sleep(10)  # Give it time to do its thing
        pyautogui.click(1015, 370)  # click download
        time.sleep(60)  # Time to download
        pyautogui.write(player) # write file name
        pyautogui.click(1190, 615, duration=0.5)  # Click save
        pyautogui.click(26, 58, duration=0.5)  # click back button
        time.sleep(10)


