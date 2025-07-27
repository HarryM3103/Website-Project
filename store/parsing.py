import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from multiprocessing import Queue
from store.exception_handling import rawHTML_Handling
from store.ProductItem import ProductItem

# TODO Finish documenting parsing.py

OK_CODE = 200
RAW_DATA = []
HARDWARE_COMPANIES = [
    "intel",
    "amd",
    "nvidia",
    "apple",
    "qualcomm",
    "broadcom",
    "microsoft",
    "samsung",
    "seagate",
    "western digital",
    "corsair",
    "asus",
    "gigabyte",
    "msi",
    "razer",
    "lenovo",
    "hp",
    "dell"
]


def data_collector(search: str, page_num: int, data_store: Queue):
    global HARDWARE_COMPANIES
    data = []
    # session = requests.Session()
    # proxies = {"http": "http://103.147.134.179:8080",
    #            "https": "http://4.245.123.244:80", }

    if search in HARDWARE_COMPANIES:
        search = f"{search} items"
    revised_search = search.replace(" ", "+")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    url = f"https://www.newegg.com/p/pl?d={revised_search}&page={str(page_num)}"

    site = urlopen(Request(url, headers=headers))

    if site.getcode() == OK_CODE:
        page = BeautifulSoup(site.read(), "html.parser")

        containers = page.find_all(
            "div", {"class": "item-cell is-blackfriday"})
        if not containers:
            containers = page.find_all(
                "div", {"class": "item-container position-relative"})

        for container in containers:
            if (container.find("i", {"class": "fas fa-info-circle-light"}) is not None):
                continue
            else:
                data_entries = rawHTML_Handling(container=container)
                data.append(data_entries)
        data_store.put(data)
    else:
        print(f"Error: {site.getcode()}")


def item_parser(data_entry: list[str]) -> ProductItem:
    product = ProductItem()
    product.image = data_entry[0]
    product.brand = data_entry[1]
    product.link = data_entry[2]
    product.name = data_entry[3]

    current_price = data_entry[4]
    previous_price = data_entry[5]
    savings = data_entry[6]
    shipping = data_entry[7]
    item_rating = data_entry[8]
    ratings = data_entry[9]
    if current_price is not None:
        try:
            product.current_price = float(current_price.split("$")[1])
        except:  # noqa: E722
            try:
                product.current_price = float(
                    current_price.split("$")[1].replace(",", ""))
            except:  # noqa: E722
                return
    if previous_price is not None:
        try:
            product.previous_price = float(previous_price.split("$")[1])
        except:  # noqa: E722
            product.previous_price = float(
                previous_price.split("$")[1].replace(",", ""))
    if savings is not None:
        try:
            product.savings = int(savings.split("%")[0])
        except:  # noqa: E722
            product.savings = 0
    if shipping is not None:
        product.shipping = shipping
    if item_rating is not None:
        product.item_rating = float(item_rating.split()[1])
    if ratings is not None:
        try:
            product.ratings_num = int(ratings)
        except:  # noqa: E722
            try:
                product.ratings_num = int(ratings.replace(",", ""))
            except:  # noqa: E722
                product.ratings_num = 0
    return product


def sort_best_value(data: list[list[str]]) -> list[str]:
    item_list: map[ProductItem] = map(item_parser, data)
    bayasian_list: list[ProductItem] = []
    for item in item_list:
        try:
            item.bayasian_calc()
            bayasian_list.append(item)
        except:  # noqa: E722
            continue
    sorted_bayasian = sorted(
        bayasian_list,
        key=lambda x: (x.bayasian_avg, -x.current_price, x.savings),
        reverse=True,
    )
    result: list[str] = []
    for item in sorted_bayasian:
        result.append(item.item_to_list())
    return result[:50]
