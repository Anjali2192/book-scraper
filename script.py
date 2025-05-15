import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

base_url = "http://books.toscrape.com/catalogue/"
current_url = base_url + "page-1.html"

product_names = []
product_price = []
product_availability = []
product_ratings = []
product_urls = []

# Define headers (User agent)
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

while True:
    r = requests.get(current_url, headers=head)
    soup = BeautifulSoup(r.text, "lxml")

    # Find all <h3> elements that contain book titles
    boxes = soup.find_all("h3")
    for box in boxes:
        title = box.find("a")["title"]
        product_names.append(title)

    # Find all <p> elements that contain book prices
    prices = soup.find_all("p", class_="price_color")
    for price in prices:
        amount = price.text
        product_price.append(amount)

    # Find all <p> elements that contain book availability
    available = soup.find_all("p", class_="instock availability")
    for avail in available:
        stock = avail.text.strip()
        product_availability.append(stock)

    # Find all <p> elements that contain book ratings
    ratings = soup.find_all("article", class_="product_pod")
    for rate in ratings:
        star_rates = rate.find("p")["class"]
        rates = star_rates[1]
        product_ratings.append(rates)

    # Find all <div> elements that contain book urls
    urls = soup.find_all("div", class_="image_container")
    for url in urls:
        links = url.find("a")["href"]
        product_urls.append(links)

    # Look for the "Next" button
    next_btn = soup.find("li", class_="next")
    if next_btn:
        next_href = next_btn.find("a")["href"]
        current_url = urljoin(current_url, next_href)  # Builds full URL for next page
    else:
        break  # No more pages

# Create dataframe
df = pd.DataFrame({"Title": product_names, "Price": product_price, "Availability": product_availability, "Star Rating": product_ratings, "URL": product_urls})

# Create csv
df.to_csv("book_details.csv", index=False)

# Create JSON
df.to_json("book_details.json", orient="records", indent=4, force_ascii=False)
