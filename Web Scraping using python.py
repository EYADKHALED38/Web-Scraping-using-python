import requests
from bs4 import BeautifulSoup
import csv

# Define the base URL and other constants
BASE_URL = "https://www.realtor.com"
SEARCH_PATH = "/realestateandhomes-search"
QUERY_PARAMS = {
    "searchType": "city",
    "location": "New+York+City_NY",
    "pgsz": 50,  # Number of results per page
    "p": None,   # Page number (will be updated dynamically)
    "sort": "relevance"  # Sort results by relevance
}
PAGE_LIMIT = 10  # Maximum number of pages to scrape

# Send a GET request to the first page of search results
QUERY_PARAMS["p"] = 1
response = requests.get(BASE_URL + SEARCH_PATH, params=QUERY_PARAMS)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the total number of search results and calculate the number of pages
total_results = int(soup.find("span", class_="srp-header__item-count").text.replace(",", ""))
total_pages = min(PAGE_LIMIT, (total_results + QUERY_PARAMS["pgsz"] - 1) // QUERY_PARAMS["pgsz"])

# Extract the property data from each page and store it in a list of dictionaries
properties = []
for page_num in range(1, total_pages + 1):
    QUERY_PARAMS["p"] = page_num
    response = requests.get(BASE_URL + SEARCH_PATH, params=QUERY_PARAMS)
    soup = BeautifulSoup(response.content, "html.parser")
    for listing in soup.find_all("div", class_="srp-item-body"):
        price = listing.find("span", class_="data-price").text.strip()
        address = listing.find("span", class_="listing-street-address").text.strip()
        city = listing.find("span", class_="listing-city").text.strip()
        state = listing.find("span", class_="listing-region").text.strip()
        zipcode = listing.find("span", class_="listing-postal").text.strip()
        beds = listing.find("span", class_="data-beds").text.strip()
        baths = listing.find("span", class_="data-baths").text.strip()
        sqft = listing.find("span", class_="data-sqft").text.strip()
        properties.append({
            "Price": price,
            "Address": address,
            "City": city,
            "State": state,
            "Zipcode": zipcode,
            "Beds": beds,
            "Baths": baths,
            "Sqft": sqft
        })

# Write the property data to a CSV file
with open("properties.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Price", "Address", "City", "State", "Zipcode", "Beds", "Baths", "Sqft"])
    writer.writeheader()
    for property in properties:
        writer.writerow(property)