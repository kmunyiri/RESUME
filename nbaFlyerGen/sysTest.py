import os
import sys
from datetime import date
import threeLetterTeams
from pathlib import Path
teams = threeLetterTeams.teams
import shutil

# today = date.today()
#
# if len(sys.argv) == 4:
#     d = sys.argv[1] + " " + sys.argv[2]
#     team = sys.argv[3]
# elif len(sys.argv) == 3:
#     d = sys.argv[1]
#     team = sys.argv[2]
# else:
#     print(" Please follow the format - wolvesPlug date team ie wolvesPlug Nov 11 Timberwolves" )
#     sys.exit()
#
# if d.lower() == "today":
#     d = today.strftime("%b %d")
#
# print(d)
# print(team)

path = Path.cwd()
os.makedirs("Teams", exist_ok=True)
for filename in os.listdir("."):
    if filename in teams:
        shutil.move(path/filename, path/"Teams"/filename)
print("done")