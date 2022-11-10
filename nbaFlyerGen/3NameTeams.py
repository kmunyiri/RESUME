# 3NameTeams.py - gets teams names for NBA
import pandas as pd
import bs4
import requests



file = open("threeLetterTeams.py","w")


url = "https://www.basketball-reference.com/leagues/NBA_2023.html"


df = pd.read_html(url)



res = requests.get(url)

res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")

table = soup.find_all("tbody")

table1 = table[0]
table2 = table[1]

# print(table2)
# # print(table1.find("th"))

link = []


# print(table1.find_all("th"))

teams1 = table1.find_all("th")

teams2 = table2.find_all("th")

names = []
file.write("teams = {\n")
for team in range(len(teams1)):

    # print(f"{teams1[team].a.text.split()}....{len(teams1[team].a.text.split())}")
    if len(teams1[team].a.text.split()) < 3:
        name = teams1[team].a.text.split()[1].strip()
    else:
        name = teams1[team].a.text.split()[2].strip()
    link = teams1[team].a["href"].strip()


    file.write(f"\"{name}\" : \"{link}\",\n")
    # names.append(name)
    # print(teams[team].a.text)
    #
    #
    # print(teams[team].a["href"])

    # link.append()
file.close()
#
file = open("threeLetterTeams.py", "a")
for team in range(len(teams2)):
    if len(teams2[team].a.text.split()) < 3:
        name = teams2[team].a.text.split()[1].strip()
    else:
        name = teams2[team].a.text.split()[2].strip()

    link = teams2[team].a["href"].strip()

    file.write(f"\"{name}\" : \"{link}\", \n")
    # names.append(name)
    #
    # print(teams[team].a["href"])
    # print(teams[team].a.text)
    # link.append(teams[team].a["href"])
#
file.write("}")




# print(len(link))
# print(link)





file.close()

# print(table[1].a["href"])


#
# print(df[1])

