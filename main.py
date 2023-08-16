from bs4 import BeautifulSoup
import json
import requests
import csv
from flask import Flask, render_template, request
from store.parsing import gpuCSV_parser, sort_best_value
from store.gpuItem import GpuItem

app = Flask(__name__)

SEARCH = ""


def data_collector(search):
    data = []
    url = "https://www.newegg.com/p/pl?d=" + search

    for pages in range(1, 15):
        site = requests.get(url + "&pages=" + str(pages))
        page = BeautifulSoup(site.content, "html.parser")

        containers = page.find_all("div", {"class": "item-container"})

        for container in containers:
            # Item Image
            item_img = container.img["src"]

            # Item link
            try:
                item_link = container.a["href"]
            except:
                item_link = None

            # Item title
            try:
                item_title = container.find("a", {"class": "item-title"}).text
            except:
                item_title = None

            # Item brand
            try:
                brand_info = container.find("div", {"class": "item-branding"}).a.img[
                    "title"
                ]
            except:
                if (item_title.split()[0].lower() == "be") or (
                    item_title.split()[0].lower() == "cooler"
                ):
                    brand_info = f"{item_title.split()[0]} {item_title.split()[1]}"
                else:
                    brand_info = item_title.split()[0]

            # Item price (current)
            try:
                item_price = (
                    "$" + container.find("li", {"class": "price-current"}).strong.text
                )
            except:
                item_price = None

            # Item's previous price
            try:
                item_previous_price = container.find(
                    "span", {"class": "price-was-data"}
                ).text
            except:
                item_previous_price = None

            # Item's savings
            try:
                item_save = container.find("span", {"class": "price-save-percent"}).text
            except:
                item_save = None

            # Item rating
            try:
                item_rating = container.find("i", {"class": "rating rating-5"})[
                    "aria-label"
                ]

            except:
                try:
                    item_rating = container.find("i", {"class": "rating rating-4-5"})[
                        "aria-label"
                    ]
                except:
                    try:
                        item_rating = container.find("i", {"class": "rating rating-4"})[
                            "aria-label"
                        ]
                    except:
                        item_rating = None

            try:
                num_ratings_raw = container.find(
                    "span", {"class": "item-rating-num"}
                ).text
                num_ratings = num_ratings_raw.split("(")[1].split(")")[0]
            except:
                num_ratings = None

            # Item shipping price
            try:
                shipping = container.find("li", {"class": "price-ship"}).text
            except:
                shipping = None

            # Group data into list
            data_entries = [
                item_img,
                brand_info,
                item_link,
                item_title,
                item_price,
                item_previous_price,
                item_save,
                shipping,
                item_rating,
                num_ratings,
            ]
            data.append(data_entries)
            print(data_entries)

    return data


# Initialize the html file
@app.route("/")
def data_parse():
    return render_template("thing.html")


# Receive the item data that the user submits
@app.route("/data_received", methods=["POST"])
def data_received():
    if request.method == "POST":  # If the request is a 'POST' request
        global SEARCH  # Declare the 'SEARCH' variable as the global variable
        SEARCH = request.form.get(
            "name"
        )  # Set the global variable to the data sent by the 'POST' request
        return ("", 204)  # return a response


# Send the data from parsing.py to javascript via AJAX
@app.route("/data_sent")
def data_sent():
    data = data_collector(
        SEARCH
    )  # Call the data_collector function that webscrapes the information from newegg.com
    info = sort_best_value(
        data
    )  # Set the variable to the return value of sort_best_value()
    return info  # return the list


if __name__ == "__main__":
    app.run(debug=True, port=8000)


# sort = sort_best_value()
# for i in sort:
#     print(i)
