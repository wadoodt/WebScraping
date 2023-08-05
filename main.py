from bs4 import BeautifulSoup
import requests

keyWord = input("What are you looking for? ")
print("")
results = []
print("Results from cheapest to most expensive (& their description & link to the product's page): ")
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
    descriptions = doc.find_all("div", {"class": "product-list-link-text"})
    linksToBeSorted = doc.find_all("div", {"class": "product-list-item"})
    links = []
    for i in linksToBeSorted:
        children = i.findChildren("a", recursive=False)
        for child in children:
            links.append(child.get("href"))

    for i in range(len(prices)):
        results.append([float(prices[i].text[1:-1]), descriptions[i].text, links[i]])
    results.sort()
    x += 1

for item in results:
    item[0] = "£"+str(item[0])
    print(item)