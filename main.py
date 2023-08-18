import json
import csv
from flask import Flask, render_template, request
from store.parsing import gpuCSV_parser, sort_best_value, data_collector
from store.gpuItem import GpuItem

app = Flask(__name__)

SEARCH = ""


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
