import requests, csv
from bs4 import BeautifulSoup

def get_each_team_stats(url, session):
    response = session.get(url)
    if response.status_code != 200:
        print('Failed to fetch the webpage. Status Code: ', response.status_code)
        exit()
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('table', id="matchlogs_for")

    headers = [th.text.strip() for th in table.find('thead').find_all('th') if th]

    body = []

    for row in table.find('tbody').find_all('tr'):
        body.append([td.text for td in row.find_all(['th', 'td'])])

    return headers, body


session = requests.Session()

# Fetching a premier league overall stats table
url="https://fbref.com/en/comps/9/Premier-League-Stats"
response = session.get(url)

# Exiting if connection failed
if response.status_code != 200:
    print("Failed to fetch the page! Status code: ", response.status_code)
    exit()


soup = BeautifulSoup(response.content, 'lxml')

# Finding the table that has premier league 2024 table
table = soup.find('table', id="results2024-202591_overall")

# Getting all the links to individual team stats
team_stats_url = [row.find('a').get('href') for row in table.find_all('td', attrs={'data-stat':'team'})]
team_names = [row.find('a').text for row in table.find_all('td', attrs={'data-stat':'team'})]
team_stats_url = [ "https://fbref.com" + team  for team in team_stats_url]

print(team_names)

# headers, _ = get_each_team_stats(team_stats_url[0], session)

# with open('team-stats.csv', mode='a', newline="", encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(headers)
#     for team in team_stats_url[:1]:
#         _, body = get_each_team_stats(team, session)
#     writer.writerows(body)

session.close()


