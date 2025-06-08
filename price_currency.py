import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"
res = requests.get(url)

soup = BeautifulSoup(res.content, "html.parser")

books = soup.find_all("article", class_="product_pod")

data = []

for b in books:
    title = b.h3.a["title"]
    price = b.find("p", class_="price_color").text
    data.append([title, price])

# Creating the csv file
with open("bookdetails.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price(original currency), Price(converted currency)"])
    writer.writerows(data)
