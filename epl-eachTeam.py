import requests, csv
from bs4 import BeautifulSoup
import time

def get_table_headers(url, session):
    response = session.get(url)
    if response.status_code != 200:
        print('Failed to fetch the webpage. Status Code: ', response.status_code)
        exit()
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('table', id="matchlogs_for")

    headers = [th.text.strip() for th in table.find('thead').find_all('th') if th]

    return headers

def get_each_team_stats(url, session):
    response = session.get(url)
    print('Fetching data from ', url)

    if response.status_code != 200:
        print('Failed to fetch the webpage. Status Code: ', response.status_code)
        exit()
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('table', id="matchlogs_for")

    body = []

    for row in table.find('tbody').find_all('tr'):
        body.append([td.text for td in row.find_all(['th', 'td'])])

    return body


requests_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://fbref.com/en/comps/9/Premier-League-Stats",
    "Upgrade-Insecure-Requests": "1",
}

session = requests.Session()
session.headers.update(requests_headers)

# Fetching a premier league overall stats table
url="https://fbref.com/en/comps/9/Premier-League-Stats"
response = session.get(url)

# Exiting if connection failed
if response.status_code != 200:
    print("Failed to fetch the page! Status code: ", response.status_code)
    print(response.headers)
    exit()


soup = BeautifulSoup(response.content, 'lxml')

# Finding the table that has premier league 2024 table
table = soup.find('table', id="results2024-202591_overall")

# Getting all the links to individual team stats
team_stats_url = [row.find('a').get('href') for row in table.find_all('td', attrs={'data-stat':'team'})]
team_names = [row.find('a').text for row in table.find_all('td', attrs={'data-stat':'team'})]
team_stats_url = [ "https://fbref.com" + team  for team in team_stats_url]

headers = get_table_headers(team_stats_url[0], session)


with open('team-stats.csv', mode='w', newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    i = 0
    for team in team_stats_url:
        writer.writerow([team_names[i]])
        body = get_each_team_stats(team, session)
        writer.writerow(headers)
        writer.writerows(body)
        writer.writerow([])
        writer.writerow([])
        i = i+1
        time.sleep(10)
    

session.close()


