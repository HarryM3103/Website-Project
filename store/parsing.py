import requests
from bs4 import BeautifulSoup
from multiprocessing import Queue
from store.ProductItem import ProductItem

# TODO Finish documenting parsing.py

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

    if search in HARDWARE_COMPANIES:
        search = f"{search} products"
    revised_search = search.replace(" ", "+")

    url = f"https://www.newegg.com/p/pl?n=4841&d={revised_search}&page={str(page_num)}"

    site = requests.get(url)
    page = BeautifulSoup(site.content, "html.parser")

    containers = page.find_all("div", {"class": "item-container"})

    for container in containers:
        if (container.find("i", {"class": "fas fa-info-circle-light"}) is not None):
            continue
        else:
            # Item Image
            item_img = container.img["src"]

            # Item link
            try:
                item_link = container.a["href"]
            except:
                item_link = None

            # Item title
            try:
                item_title = container.find(
                    "a", {"class": "item-title"}).text
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
                    "$" +
                    container.find(
                        "li", {"class": "price-current"}).strong.text
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
                item_save = container.find(
                    "span", {"class": "price-save-percent"}).text
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
                shipping = container.find(
                    "li", {"class": "price-ship"}).text
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
    data_store.put(data)


def item_parser(data_entry: list[str]) -> ProductItem:
    product = ProductItem()
    product.image = data_entry[0]
    product.brand = data_entry[1]
    product.link = data_entry[2]
    product.name = data_entry[3]
    if data_entry[4] is not None:
        try:
            product.current_price = float(data_entry[4].split("$")[1])
        except:
            try:
                product.current_price = float(
                    data_entry[4].split("$")[1].replace(",", ""))
            except:
                return
    if data_entry[5] is not None:
        try:
            product.previous_price = float(data_entry[5].split("$")[1])
        except:
            product.previous_price = float(
                data_entry[5].split("$")[1].replace(",", ""))
    if data_entry[6] is not None:
        try:
            product.savings = int(data_entry[6].split("%")[0])
        except:
            product.savings = 0
    if data_entry[7] is not None:
        product.shipping = data_entry[7]
    if data_entry[8] is not None:
        product.item_rating = float(data_entry[8].split()[1])
    if data_entry[9] is not None:
        try:
            product.ratings_num = int(data_entry[9])
        except:
            try:
                product.ratings_num = int(data_entry[9].replace(",", ""))
            except:
                product.ratings_num = 0
    return product


def sort_best_value(data: list[list[str]]) -> list[str]:
    item_list: map[ProductItem] = map(item_parser, data)
    bayasian_list: list[ProductItem] = []
    for item in item_list:
        try:
            item.bayasian_calc()
            bayasian_list.append(item)
        except:
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
