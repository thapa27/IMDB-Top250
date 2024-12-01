import requests
from bs4 import BeautifulSoup

url = "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats"

response = requests.get(url)
if response.status_code != 200:
    print('Failed to fetch the webpage. Status Code: ', response.status_code)
    exit()
soup = BeautifulSoup(response.content, 'lxml')

table = soup.find('table', id="matchlogs_for")

headers = [th.text.strip() for th in table.find('thead').find_all('th') if th]

body = []

for row in table.find('tbody').find_all('tr'):
    body.append([td.text for td in row.find_all(['th', 'td'])])


