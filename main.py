import json
import threading
from queue import Queue
import csv
from flask import Flask, render_template, request
from store.parsing import sort_best_value, data_collector
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
    data = []
    pure_data = []
    threads = []
    q = Queue()
    for i in range(14):
        t = threading.Thread(target=data_collector, args=(SEARCH, i, q,))
        t.daemon = True
        threads.append(t)

    for i in range(14):
        threads[i].start()

    for i in range(14):
        threads[i].join()

    for info in list(q.get()):
        pure_data.append(info)
    info = sort_best_value(
        pure_data
    )  # Set the variable to the return value of sort_best_value()
    return info  # return the list


if __name__ == "__main__":
    app.run(debug=True, port=8000)


# sort = sort_best_value()
# for i in sort:
#     print(i)
