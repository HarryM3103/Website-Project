import json
import threading
from queue import Queue
import csv
from flask import Flask, render_template, request
from store.parsing import sort_best_value, data_collector
from store.ProductItem import ProductItem


app = Flask(__name__)

SEARCH = ""
PAGES_TO_SEARCH = 14


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


def threading_search():
    pure_data = []  # Declare the optimized data list, pure_data
    threads = []  # Declare the threads list
    q = Queue()  # Instantiate the queue object

    # Make as many threads as there are pages to search
    for i in range(PAGES_TO_SEARCH):
        # Instantiate the the thread, giving the "data_collector()" as the target function
        t = threading.Thread(target=data_collector, args=(SEARCH, i, q,))
        t.daemon = True  # Set daemon to true
        threads.append(t)  # Append the thread to the threads list

    # Loop through the threads list and start the threads
    for i in range(PAGES_TO_SEARCH):
        threads[i].start()

    # Loop through the threads list and join the threads
    for i in range(PAGES_TO_SEARCH):
        threads[i].join()

    # Loop throught the queue containing the raw data from "data_collector()"
    for info in list(q.get()):
        # Append the raw data to the optimized data list
        pure_data.append(info)
    info = sort_best_value(
        pure_data
    )  # Set the variable, info,  to the return value of sort_best_value()
    return info
    # Send the data from parsing.py to javascript via AJAX


@app.route("/data_sent")
def data_sent():
    frontend_info = threading_search()
    return frontend_info   # return the info to the frontend


if __name__ == "__main__":
    app.run(debug=True, port=8000)


# sort = sort_best_value()
# for i in sort:
#     print(i)
