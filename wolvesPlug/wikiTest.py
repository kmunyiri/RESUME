import bs4
import requests
import os
import pprint
def getTeamName(team):
    """ Given full City and Team Name will return only Team Name"""
    # teamName = ""
    if len(team.split()) < 3:
        return team.split()[1]
    else:
        return team.split()[2]

def wikiLogo(name):
    """Retrieves Logo from Wikipedia page"""
    url = "https://en.wikipedia.org/wiki/"
    team = name.split()
    wikiName = "_".join(team)

    res = requests.get(url + wikiName)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    table = soup.find_all("img")
    # pprint.pprint(table)
    # print(len(table))

    for link in table:
        if link["alt"] == name + " logo":
            print("row found")
            print(name + " logo")
            print("http://" + link["srcset"].split()[-2])
    # # test = soup.find_all("tbody")
    # print(f"{name}...{len(table)}")
    # print(table)
    # if len(table) < 2:
    #     table = soup.find_all("tbody")[1].find_all("img")
    #
    #
    # link = "http://" + table[0]["srcset"].split(",")[1].split()[0][2:]
    # link =  table[0]["srcset"]
    # print(link)
    #
    # print(f"Printing {team} logo.......")
    #
    # r = requests.get(link)
    # r.raise_for_status()
    # teamName = getTeamName(name)
    # iFile = open(os.path.join(teamName, "logo.jpg"), "wb")
    #
    # for chunk in r.iter_content(100000):
    #     iFile.write(chunk)
    # iFile.close()

    print("Created and saved")


wikiLogo("Minnesota Timberwolves")
wikiLogo("San Antonio Spurs")