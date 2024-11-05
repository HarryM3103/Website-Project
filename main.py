import multiprocessing as mp
from multiprocessing import Queue
from flask import Flask, render_template, request
from store.parsing import sort_best_value, data_collector


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


def processing_search():
    pure_data = []  # Declare the optimized data list, pure_data
    processes = []  # Declare the processes list
    raw_data: list[Queue] = []

    q = Queue()
    data_collector(SEARCH, 1, q)

    # Make as many processes as there are pages to search
    for i in range(PAGES_TO_SEARCH):
        q = Queue()
        p = mp.Process(target=data_collector, args=(SEARCH, i+1, q,))  # Instantiate the process, giving the "data_collector()" as the target function
        p.daemon = True
        processes.append(p)  # Append the process to the processes list
        raw_data.append(q)

    # Loop through the processes list and start the processes
    for i in range(PAGES_TO_SEARCH):
        processes[i].start()

    # Loop through the queue containing the raw data from "data_collector()"
    for queue in raw_data:
        for info in list(queue.get()):
            pure_data.append(info)
    info = sort_best_value(
        pure_data
    )  # Set the variable, info,  to the return value of sort_best_value()
    return info
    # Send the data from parsing.py to javascript via AJAX


@app.route("/data_sent")
def data_sent():
    frontend_info = processing_search()
    return frontend_info   # return the info to the frontend


if __name__ == "__main__":
    app.run(debug=True, port=8000)


# sort = sort_best_value()
# for i in sort:
#     print(i)
