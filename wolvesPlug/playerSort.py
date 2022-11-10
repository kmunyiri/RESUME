# playerSort.py - sorts players into their respective folders

import os
import pyautogui
from pathlib import Path
import time
import shutil
import threeLetterTeams

teams = threeLetterTeams.teams
cwd = Path.cwd()
def teamCount():
    t = 0
    for folder in os.listdir(cwd):
        if folder in teams:
            print(folder)
            t += 1
            del teams[folder]
    print(t)
    print(teams)

# for player in os.listdir(cwd / "PlayerSort"):
#     basename = Path(cwd / "PlayerSort" / player).stem
#     print(basename.split())
#     if len(basename.split()) > 2:
#         team = basename.split()[0]
#         position = basename.split()[1]
#         name = basename.split()[2]
#         os.makedirs(cwd / team / position, exist_ok=True)
#         shutil.copy(cwd / "PlayerSort" / player, cwd / team / position / (name + ".png"))
#

print("done")

teamCount()
print(teams)