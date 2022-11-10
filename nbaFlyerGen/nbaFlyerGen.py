# nbaFlyerGen - usage: nbaFlyerGen.py date team

# if nbaFlyerGen today Timberwolves - will Timberwolves for current day

# if nbaFlyerGen Nov 11 Timberwolves - will make flyer for Timberwolves for Nov 11

# if nbaFlyerGen today all - will make flyers for every game that day

# if nbaFlyerGen Nov 11 all - will make flyer for every game on NOV 11


import bs4
import requests
from requests_html import HTMLSession
from pprint import pprint
import pandas as pd
import sys
from PIL import Image, ImageDraw
from PIL import ImageFont
import os
from datetime import date
from datetime import datetime
import random
import glob
import threeLetterTeams
import unidecode  # to handle the names of foreign players
import time
import pprint

teams = threeLetterTeams.teams


def fileFinder(path):
    """ Given a path will return a random file in the folder """
    rlist = []
    if os.path.exists(path):
        for filename in os.listdir(path):
            if not filename.startswith("."):
                rlist.append(filename)
        return random.choice(rlist)
    else:
        print(f"{path} does not exist. Try a different position")
        raise FileNotFoundError


def smart_resize(input_image, new_size):
    """ Attempt to standardize pngs of the given image object"""
    width = input_image.width
    height = input_image.height

    # Image is portrait or square
    if height >= width:
        crop_box = (0, (height - width) // 2, width, (height - width) // 2 + width)
        return input_image.resize(size=(new_size, new_size),
                                  box=crop_box)

    # Image is landscape
    if width > height:
        crop_box = ((width - height) // 2, 0, (width - height) // 2 + height, height)

        return input_image.resize(size=(new_size, new_size),
                                  box=crop_box)


def playerResize(player, size):
    width, height = player.size
    ratio1 = width / height
    ratio2 = height / width
    newWidth = 450
    newHeight = 800

    # If square just resize
    if width / height < 1.5:
        return smart_resize(player, 550)

    elif height > newHeight:
        return player.resize((int(ratio1 * newHeight), newHeight))
    elif width > newWidth:
        return player.resize((newWidth, int(ratio2 * newWidth)))


def getTeamName(team):
    """ Given full City and Team Name will return only Team Name"""
    # teamName = ""
    if len(team.split()) < 3:
        return team.split()[1]
    else:
        return team.split()[2]


def getPlayer(name, team):
    """ Given player and team that he plays for returns link to player on basketball-reference"""
    print(f"Looking for {name} on the {team}.....")
    url = "https://www.basketball-reference.com"

    if len(team.split()) < 3:
        teamName = team.split()[1]
    else:
        teamName = team.split()[2]
    link = teams[teamName]

    teamLink = url + link

    # teamdf = pd.read_html(teamLink)

    res = requests.get(teamLink)

    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    table = soup.find_all("tbody")[0]

    players = table.find_all("tr")

    link = []
    for player in range(len(players)):
        if unidecode.unidecode(players[player].a.text.split()[1].lower()) == name.lower():
            print(f"player {players[player].a.text} found")
            print(url + players[player].a["href"])
            return url + players[player].a["href"]


def getStats(df):
    """  Given table of player it will retrieve the stats for the current season and return that   """
    szn = "2022-23"
    stats = {}
    s = 0
    for i in range(len(df[1])):
        if df[1].loc[i][0] == szn:
            # print(df[1].loc[i])
            s = i
    # print(df1[1].loc[s])
    stats["PTS"] = df[1].loc[s][29]
    stats["REB"] = df[1].loc[s][23]
    stats["AST"] = df[1].loc[s][24]

    return stats


def wikiLogo(name):
    """Retrieves Logo from Wikipedia page"""
    url = "https://en.wikipedia.org/wiki/"
    team = name.split()
    wikiName = "_".join(team)

    res = requests.get(url + wikiName)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    table = soup.find_all("img")

    for links in table:
        if links["alt"] == name + " logo":
            link = "http:" + links["srcset"].split()[-2]
            print(link)
    print(f"Printing {team} logo.......")

    r = requests.get(link)
    r.raise_for_status()
    teamName = getTeamName(name)
    iFile = open(os.path.join(teamName, "logo.jpg"), "wb")

    for chunk in r.iter_content(100000):
        iFile.write(chunk)
    iFile.close()

    print("Created and saved")


def getLogo(team):
    """Given a team will retrieve its logo open it as an image which is returned """
    if os.path.exists(os.path.join(getTeamName(team), "logo.jpg")):
        logo = Image.open(os.path.join(getTeamName(team), "logo.jpg")).convert("RGBA").resize((120, 120))
    else:
        wikiLogo(team)
        logo = Image.open(os.path.join(getTeamName(team), "logo.jpg")).convert("RGBA").resize((120, 120))
    return logo


def getRecord(team):
    """ Given team retrieves current record """
    url = "https://www.basketball-reference.com/"

    res = requests.get(url + teams[team])
    print(url + teams[team])

    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    record = soup.find_all("p")[2].text.split()[1][:-1]

    # print(opt)
    return record


def makeFlyer(match):
    """" Main function that creates the flyer by handling printing when passed a team """
    team1 = match["visiting team"]
    teamName1 = getTeamName(team1)

    team2 = match["home team"]
    teamName2 = getTeamName(team2)

    position1 = "SG"
    position2 = "SG"

    # Flyer creation
    W, H = 1080, 1080  # standard size of flyer
    im = Image.new("RGBA", (W, H), "white")  # create 1080x1080 image for flyer

    position = ["PG", "SG", "SF", "PF", "C"]
    try:
        filename1 = fileFinder(os.path.join(teamName1, position1))
    except FileNotFoundError:
        while not os.path.exists(os.path.join(teamName1, position1)):
            print(f"There is no {position1} in {teamName1}")
            position1 = random.choice(position)
        filename1 = fileFinder(os.path.join(teamName1, position1))

    try:
        filename2 = fileFinder(os.path.join(teamName2, position2))
    except FileNotFoundError:
        while not os.path.exists(os.path.join(teamName2, position2)):
            print(f"There is no {position2} in {teamName2}")
            position2 = random.choice(position)
        filename2 = fileFinder(os.path.join(teamName2, position2))

    name1 = filename1.split(".")[0]
    name2 = filename2.split(".")[0]

    p1 = getPlayer(name1, team1)
    p2 = getPlayer(name2, team2)

    # Read player page
    df1 = pd.read_html(p1)
    df2 = pd.read_html(p2)

    # Grab the Stats for the two players
    stats1 = getStats(df1)
    stats2 = getStats(df2)

    # Load player images
    player1 = Image.open(os.path.join(teamName1, position1, filename1)).convert("RGBA")
    player2 = Image.open(os.path.join(teamName2, position2, filename2)).convert("RGBA")

    # Size them appropriately
    player1 = smart_resize(player1, 550)
    player2 = smart_resize(player2, 550)

    draw = ImageDraw.Draw(im)  # make Draw object
    font = ImageFont.truetype(os.path.join("cabal-font", "Cabal-w5j3.ttf"), 30)

    draw.text((450 / 2, 50), team1, fill="black", font=font, anchor="mm")
    draw.text((855, 50), team2, fill="black", font=font, anchor="mm")

    w2, h2 = player1.size
    im.paste(player1, (int((450 - w2) / 2), int((900 - h2) / 2)), player1)

    w3, h3 = player2.size
    im.paste(player2, (int((1710 - w3) / 2), int((900 - h3) / 2)), player2)

    # Change size of arena based on length
    draw.text((1080 / 2, 50), match["arena"], fill="black", font=font, anchor="mm")

    print(team1)
    print(team2)

    # Team and NBA Logos
    vLogo = getLogo(team1)
    vW, vH = vLogo.size
    im.paste(vLogo, (int((1080 - vW) / 2), 300), vLogo)

    hLogo = getLogo(team2)
    hW, hH = hLogo.size
    im.paste(hLogo, (int((1080 - hW) / 2), 610), hLogo)

    draw.text((1080 / 2, 1080 / 2), "VS", fill="black", font=font, anchor="mm")

    logo = Image.open("nbaLogo.png").convert("RGBA")
    logo = logo.resize((100, 180))
    w4, h4 = logo.size
    im.paste(logo, (int((1080 - w4) / 2), 880), logo)

    # Add record
    record1 = getRecord(teamName1)
    record2 = getRecord(teamName2)

    draw.text((450 / 2, 790), record1, fill="black", font=font, anchor="mm")
    draw.text((855, 790), record2, fill="black", font=font, anchor="mm")

    # Stats
    i = 0
    for key, value in stats1.items():
        stat = f"{str(value)} {key}"
        draw.text((450 / 2, 850 + i), stat, fill="black", font=font, anchor="mm")
        i += 50
    i = 0
    for key, value in stats2.items():
        stat = f"{str(value)} {key}"
        draw.text((855, 850 + i), stat, fill="black", font=font, anchor="mm")
        i += 50

    im.show()


today = date.today()

if len(sys.argv) == 4:
    d = sys.argv[1] + " " + sys.argv[2]
    t = sys.argv[3]
elif len(sys.argv) == 3:
    d = sys.argv[1]
    t = sys.argv[2]
else:
    print(" Please follow the format - nbaFlyerGen date team ie nbaFlyerGen Nov 11 Timberwolves")
    sys.exit()

if d.lower() == "today":
    day = int(today.strftime("%d"))
    m = today.strftime("%b")
    d = m + " " + str(day)

search = d
team = t

print(search)
print(t)
# Formatting the date
month = datetime.strptime(search, "%b %d")
month = month.strftime("%B").lower()

if month != "October":
    df = pd.read_html(f"https://www.basketball-reference.com/leagues/NBA_2023_games-{month}.html")
else:
    df = pd.read_html("https://www.basketball-reference.com/leagues/NBA_2023_games.html")

games = []  # list of dictionarys

p1Stats = {}
p2Stats = {}

# Format Date, Vistor, Home, Arena
for i in range(len(df[0])):
    date = df[0].loc[i][0].split(",")
    match = {}
    if search == date[1].strip() and team == "All":
        print(f"{df[0].loc[i][2]} v. {df[0].loc[i][4]} ")
        match["date"] = df[0].loc[i][0]
        match["visiting team"] = df[0].loc[i][2]
        match["home team"] = df[0].loc[i][4]
        match["arena"] = df[0].loc[i][9]
        games.append(match)

    if search == date[1].strip() and (team in df[0].loc[i][2] or team in df[0].loc[i][4]):
        print(f"{df[0].loc[i][2]} v. {df[0].loc[i][4]} ")

        match["date"] = df[0].loc[i][0]
        match["visiting team"] = df[0].loc[i][2]
        match["home team"] = df[0].loc[i][4]
        match["arena"] = df[0].loc[i][9]
        games.append(match)

print(games)

for match in games:
    makeFlyer(match)

    time.sleep(15)

print("done")
