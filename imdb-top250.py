from bs4 import BeautifulSoup
from selenium import webdriver
import csv

driver = webdriver.Chrome()


# Fetching the webpage
url = "https://www.imdb.com/chart/top/"

driver.get(url)
html = driver.page_source
driver.quit()

# Parsing the HTML
soup = BeautifulSoup(html, "lxml")

# Extracting the movie data
movies = []
list_items = soup.find_all('li', class_="ipc-metadata-list-summary-item")


for item in list_items:
    movie_string = item.find("h3", class_="ipc-title__text").text
    rank, name = movie_string.split(". ", 1)
    year = item.find_all("span", class_="eaXxft")[0].text
    duration = item.find_all("span", class_="eaXxft")[1].text
    try:
        pg = item.find_all("span", class_="eaXxft")[2].text
    except:
        pg = "N/A"
    rating = item.find("span", class_="ipc-rating-star--rating").text
    voteCount = item.find("span", class_="ipc-rating-star--voteCount").text
    voteCount = voteCount.replace("\xa0", "")
    movies.append({"rank": rank, "name": name, "year": year, "duration": duration, "PG": pg, "rating": rating, "voteCount": voteCount})


output_file = "imdb-top-250.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=['rank', 'name', 'year', 'duration', 'PG', 'rating', 'voteCount'])
    writer.writeheader()
    writer.writerows(movies)

print(f"Data saved to {output_file} successfully!")
    


    
    
    