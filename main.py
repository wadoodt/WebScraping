from bs4 import BeautifulSoup
import requests

keyWord = input("What are you looking for? ")
print("")


x = 1
while True:
    url = f"https://www.medino.com/search?q={keyWord}&up-to-page={x}"  # searching through medical online retailer
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    a = doc.find(string="No products here yet. We're working hard on adding more products all the time, so please check "
                        "back later.")
    if a is not None:
        break
    prices = doc.find_all("span", {"class": "product-list-price-span"})
    description = doc.find_all("div", {"class": "product-list-link-text"})
    for i in range(len(prices)):
        print(description[i].text, " -- ", prices[i].text)
    x += 1
