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
# Make change later to reflect more positionless nature of the NBA
position = ["PG", "SG", "SF", "PF", "C"]

font = ImageFont.truetype(os.path.join("cabal-font", "Cabal-w5j3.ttf"), 27)

def getArguments():
    """ Gets arguments for date and team. Also handles formatting of dates """
    if len(sys.argv) == 4:
        d = sys.argv[1] + " " + sys.argv[2]
        t = sys.argv[3]
    elif len(sys.argv) == 3:
        d = sys.argv[1]
        t = sys.argv[2]
    else:
        print(" Please follow the format: nbaFlyerGen.py date team ie. nbaFlyerGen.py Nov 11 Timberwolves")
        sys.exit()
    if d.lower() == "today":
        day = int(today.strftime("%d"))
        m = today.strftime("%b")
        d = m + " " + str(day)
    return d,t 

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

def searchPosition(team, p):
    """ Given a team and position it will return a filename for a player of a certain position
     if it cant find one it will search until it finds something """
     
    while not os.path.exists(os.path.join("Teams",team, p)):
        print(f"There is no {p} in {team}")
        p = random.choice(position)
    filename = fileFinder(os.path.join("Teams",team, p))
    return [filename, p]
   
def getPage(time):
    """Given date it will format and return the proper link to scrape """
    month = datetime.strptime(time, "%b %d")
    month = month.strftime("%B").lower()

    if month != "October":
        dataframe = pd.read_html(f"https://www.basketball-reference.com/leagues/NBA_2023_games-{month}.html")
    else:
        dataframe = pd.read_html("https://www.basketball-reference.com/leagues/NBA_2023_games.html")

    return dataframe

def aspectResizeLogo(logo, size):
    """ Helps resize logos accordingly """
    # wider than it is tall
    width, height = logo.size
    # if width / height > 1:
    ratio = width / height
    return logo.resize((int(ratio * size), size))

def aspectResize(image, size):
    """ Given a player image and a size it will adjust the image accordingly so they are close in scale """
    # images given will be generally square or have a smaller with in comparison to height; also it will occupy a 450x800 space roughly 
    image = cropImage(image)
    width, height = image.size
    if width / height > 1:
        # make em skinny - ie. 1800/1000 = 1.8 so we would wanna reduce the width
        ratio = height / width
        newWidth = int(ratio * size)
        return image.resize((newWidth, size))

    elif width / height < 1:
        # thicken em up - ie. 1000/1800 = 0.8 so we would wanna increase the height
        ratio = width / height
        newHeight = int(ratio * size)
        return image.resize((newHeight, size))

    else:
        return image.resize((size, size))

def cropImage(image):
    """ Returns cropped version of image for optimal sizing """
    imageBox = image.getbbox()
    return image.crop(imageBox)
    
def getTeamName(team):
    """ Given full City and Team Name will return only Team Name """
    # teamName = ""
    if len(team.split()) < 3:
        return team.split()[1]
    else:
        return team.split()[2]
def getArenaName(arena):
    """Given an arena name it breaks it up for formatting purposes [Arena Name, Arena Type]"""
    if len(arena.split()) == 3:
        return [arena.split()[0] + " " + arena.split()[1], arena.split()[2]]
    else:
        return [arena.split()[0], arena.split()[1]]

def getGames(df, search, team):
    """ Returns list of dictionaries representing information about matches for given date for team depending on arguments """
    games = []
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
    return games

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
    for i in range(len(df[0])):
        if df[0].loc[i][0] == szn:
            # print(df[1].loc[i])
            s = i
    # print(df1[1].loc[s])
    stats["PTS"] = df[0].loc[s][29]
    stats["REB"] = df[0].loc[s][23]
    stats["AST"] = df[0].loc[s][24]

    return stats

def printStats(s,draw,x):
    """Given a stat dictionary, draw object and x prints stats under the given x on the draw object"""
    i = 0
    for key, value in s.items():
        stat = f"{str(value)} {key}"
        draw.text((x, 850 + i), stat, fill="black", font=font, anchor="mm")
        i += 50
    
def printTeamText(draw,text1, x1, y1, text2, x2, y2):
    draw.text((x1, y1), text1, fill="black", font=font, anchor="mm")
    draw.text((x2, y2), text2, fill="black", font=font, anchor="mm")

def wikiLogo(name):
    """ Retrieves Logo from Wikipedia page """
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
    iFile = open(os.path.join("Teams",teamName, "logo.jpg"), "wb")

    for chunk in r.iter_content(100000):
        iFile.write(chunk)
    iFile.close()

    print("Created and saved")


def getLogo(team):
    """ Given a team will retrieve its logo open it as an image which is returned """
    if os.path.exists(os.path.join("Teams",getTeamName(team), "logo.jpg")):
        logo = Image.open(os.path.join("Teams",getTeamName(team), "logo.jpg")).convert("RGBA").resize((120, 120))
    else:
        wikiLogo(team)
        logo = Image.open(os.path.join("Teams",getTeamName(team), "logo.jpg")).convert("RGBA").resize((120, 120))
    return aspectResizeLogo(logo,120)

def leagueLogo(image):
    """Prints NBA League Logo onto given image object"""
    logo = Image.open("nbaLogo.png").convert("RGBA")
    logo = logo.resize((100, 180))
    w4, h4 = logo.size
    image.paste(logo, (int((1080 - w4) / 2), 880), logo)

def logoPaste(visit,home,image):
    """ Given home and visiting team it will print their logo on the given image object"""
    logo1 = getLogo(visit)
    vW, vH = logo1.size
    image.paste(logo1, (int((1080 - vW) / 2), 300), logo1)

    logo2 = getLogo(home)
    hW, hH = logo2.size
    image.paste(logo2, (int((1080 - hW) / 2), 610), logo2)

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

    # TODO: Make function or dictionary for team name 
    team1 = match["visiting team"]
    teamName1 = getTeamName(team1)

    team2 = match["home team"]
    teamName2 = getTeamName(team2)


    # Start position as Shooting Guard because I generally have those 
    position1 = "SG"
    position2 = "SG"

    # Flyer creation
    W, H = 1080, 1080  # standard size of flyer
    im = Image.new("RGBA", (W, H), "white")  # create 1080x1080 image for flyer


    # Find random player of matching position in corresponding team folders 
    sp1 = searchPosition(teamName1, position1)
    filename1 = sp1[0]
    position1 = sp1[1]

    sp2 = searchPosition(teamName2, position2)
    filename2 = sp2[0]
    position2 = sp2[1]

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
    player1 = Image.open(os.path.join("Teams",teamName1, position1, filename1)).convert("RGBA")
    player2 = Image.open(os.path.join("Teams",teamName2, position2, filename2)).convert("RGBA")

    # Size them appropriately
    player1 = aspectResize(player1, 550)
    player2 = aspectResize(player2, 550)

    draw = ImageDraw.Draw(im)  # make Draw object
    # font = ImageFont.truetype(os.path.join("cabal-font", "Cabal-w5j3.ttf"), 27)

    printTeamText(draw, team1, 450/2,50, team2,855,50)
    # draw.text((450 / 2, 50), team1, fill="black", font=font, anchor="mm")
    # draw.text((855, 50), team2, fill="black", font=font, anchor="mm")

    w2, h2 = player1.size
    im.paste(player1, (int((450 - w2) / 2), int((900 - h2) / 2)), player1)

    w3, h3 = player2.size
    im.paste(player2, (int((1710 - w3) / 2), int((900 - h3) / 2)), player2)

    # Arena name
    arena = getArenaName(match["arena"])
    printTeamText(draw, arena[0], 1080/2, 50, arena[1], 1080/2, 75)
    # draw.text((1080 / 2, 50), arena[0], fill="black", font=font, anchor="mm")
    # draw.text((1080 / 2, 75), arena[1], fill="black", font=font, anchor="mm")


    print(team1)
    print(team2)

    # Team and NBA Logos    
    logoPaste(team1,team2, im)
    draw.text((1080 / 2, 1080 / 2), "VS", fill="black", font=font, anchor="mm")
    leagueLogo(im)
    
    # Add record
    record1 = getRecord(teamName1)
    record2 = getRecord(teamName2)
    printTeamText(draw, record1, 450/2, 790, record2, 855, 790)
    # draw.text((450 / 2, 790), record1, fill="black", font=font, anchor="mm")
    # draw.text((855, 790), record2, fill="black", font=font, anchor="mm")

    printStats(stats1, draw, 450/2)
    printStats(stats2, draw, 855)

    im.show()

today = date.today()

args = getArguments()
search = args[0]
team = args[1]


df = getPage(search)

games = getGames(df, search, team)

print(games)

for match in games:
    makeFlyer(match)

    time.sleep(15)

print(f"{search} Games for {team} printed  ")
