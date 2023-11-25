import tkinter as tk
from bs4 import BeautifulSoup
import requests
import webbrowser


results = []

def update_results():
    global results
    results.clear()
    # Get the text from the entry
    text = entry.get()
    if text == "":
        header.config(text="Search on medino.com")
        results_list.delete(0, tk.END)
        return
    x = 1
    links = []
    urls = []
    while True:
        url = f"https://www.medino.com/search?q={text}&up-to-page={x}"  # searching through medical online retailer
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        a = doc.find(
            string="No products here yet. We're working hard on adding more products all the time, so please check "
                   "back later.")
        b = doc.find("div", {"id":"no-search-results-page"})
        if b is not None:
            header.config(text=f"No results for {text}")
            results_list.delete(0, tk.END)
            return
        if a is not None:
            if x == 1:
                header.config(text=f"No results for {text}")
                results_list.delete(0, tk.END)
                return
            break
        prices = doc.find_all("span", {"class": "product-list-price-span"})
        descriptions = doc.find_all("div", {"class": "product-list-link-text"})
        linksToBeSorted = doc.find_all("div", {"class": "product-list-item"})
        for i in linksToBeSorted:
            children = i.findChildren("a", recursive=False)
            for child in children:
                links.append(child.get("href"))

        for i in range(len(prices)):
            results.append([float(prices[i].text[1:-1]), descriptions[i].text])
            urls.append("www.medino.com" + links[i])
        results.sort()
        x += 1

    for item in results:
        item[0] = "£" + str(item[0])
    # Update the header text
    header.config(text=f"Results for {text}")

    # Clear previous list items
    results_list.delete(0, tk.END)

    for result in results:
        results_list.insert(tk.END, result)

    # Store the URLs as a data attribute in the listbox
    results_list.urls = urls


def on_result_click(event):
    # Get the clicked item's index
    index = results_list.curselection()[0]

    # Get the URL associated with the clicked item's index
    url = results_list.urls[index]

    # Open the URL in a web browser
    webbrowser.open_new(url)


# Create a new tkinter window
root = tk.Tk()
root.title("Search on medino.com online pharmacy")

# Header label
header = tk.Label(root, text="Search on medino.com", font=("Arial", 14))
header.pack()

# Entry for user input
entry = tk.Entry(root)
entry.pack()

# Button to trigger results update
button = tk.Button(root, text="Show Results", command=update_results)
button.pack()

# Listbox to display results
results_list = tk.Listbox(root, width=200, height=50)
results_list.pack()

# Bind click event to the Listbox
results_list.bind('<Double-Button-1>', on_result_click)

# Run the main Tkinter loop
root.mainloop()