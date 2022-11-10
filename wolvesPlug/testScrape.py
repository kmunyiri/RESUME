# testScrape.py - testing scraping from basketballreference.com to use for project
import bs4
import requests

url = "https://www.basketball-reference.com/leagues/NBA_2023_games.html"
res = requests.get(url)
res.raise_for_status()

resSoup = bs4.BeautifulSoup(res.text, "html.parser")


# # Verify tables and classes
# print("Classes of each table:")
# for table in resSoup.findAll("table"):
#     print(table.get("class"))

tables = resSoup.find_all("table")
table = resSoup.find("table", class_="sortable")
print(table)

for row in table.tbody.findAll("tr"):
    columns = row.find_all("td")

    if(columns != []):
        print(columns[0].text)