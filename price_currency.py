import requests
from bs4 import BeautifulSoup
import csv # csv file
import re # regular expression module

# API configuration
api_key = "847ef14a1cf22a0850159e17"
base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/"

# Fetch real-time exchange rates
def get_exchange_rate(base_currency, target_currency):
    url = base_url + base_currency
    response = requests.get(url) # fetching the data from the api

    if response.status_code == 200: # 200 means everything is working well
        data = response.json() # convert the data from the api from JSON format to a python dictionary to enable easy access
        exchange_rate = data['conversion_rates'][target_currency] # gets all of the nestes conversion rates-'conversion_rates', gets the specific rate for that currency-target_currency 
        return exchange_rate
    else:
        print("Error fetching exchange rates")
        return None

# Convert currency using exchange rate
def convert_currency(amount, base_currency, target_currency):
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate is not None:
        return round(amount * exchange_rate, 2) # rounds it off to 2dp
    else:
        return None

# Scrape book prices and convert them
def scrape_books_and_convert(target_currency):
    url = "https://books.toscrape.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    data = []

    for b in books:
        title = b.h3.a["title"]
        price_text = b.find("p", class_="price_color").text  # Format: '£53.74'
        price_gbp = float(re.findall(r"[\d.]+", price_text)[0])  # Extract numeric part
        converted_price = convert_currency(price_gbp, "GBP", target_currency) # Conversion

        data.append([title, f"£{price_gbp: .2f}", f"{converted_price:.2f} {target_currency}"])

    return data

# Main execution
def main():
    print("Welcome to the Book Price Scraper & Currency Converter")

    target_currency = input("Enter target currency (ex; USD, EUR): ").upper()

    book_data = scrape_books_and_convert(target_currency)

    # Save to CSV
    with open("bookdetails.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price (GBP)", f"Price ({target_currency})"])
        writer.writerows(book_data)

    print("Book data with converted prices has been saved to 'bookdetails.csv'.")

if __name__ == "__main__":
    main()

