from bs4 import BeautifulSoup
import requests, csv

url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# Sending an HTTP request to the URL
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch the page. Status Code: ", response.status_code)
    exit()

# Parsing the page content
soup = BeautifulSoup(response.content, 'lxml')

#Finding the table with team stats
table = soup.find("table", id="results2024-202591_overall")
headers = [th.text for th in table.find_all('th') if th.get('aria-label')]

tbody = table.find("tbody")

rows = []

for row in tbody.find_all('tr'):
    cells = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
    rows.append(cells)

rows = [row[:-1] for row in rows]
headers = headers[:-1]

output_file = 'epl.csv'

with open(output_file, mode='w', newline="", encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(headers)
    writer.writerows(rows)


# combining header keys with its respective values
# table_stats = []

# for row in range(len(rows)):
#     table_stats.append({headers[i]:rows[row][i] for i in range(len(headers))})
