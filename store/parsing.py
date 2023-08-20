import csv
import requests
from bs4 import BeautifulSoup
from store.gpuItem import GpuItem


def data_collector(search):
    data = []
    revised_search = search.replace(" ", "+")
    url = "https://www.newegg.com/p/pl?d=" + revised_search

    for pages in range(1, 15):
        site = requests.get(url + "&pages=" + str(pages))
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
                print(data_entries)
    return data


def gpuCSV_parser(data):
    gpu_List: list[GpuItem] = []
    for entries in data:
        gpu = GpuItem()
        gpu.image = entries[0]
        gpu.brand = entries[1]
        gpu.link = entries[2]
        gpu.name = entries[3]
        if entries[4] is not None:
            try:
                gpu.current_price = float(entries[4].split("$")[1])
            except:
                gpu.current_price = float(
                    entries[4].split("$")[1].replace(",", ""))
        if entries[5] is not None:
            try:
                gpu.previous_price = float(entries[5].split("$")[1])
            except:
                gpu.previous_price = float(
                    entries[5].split("$")[1].replace(",", ""))
        if entries[6] is not None:
            gpu.savings = int(entries[6].split("%")[0])
        if entries[7] is not None:
            gpu.shipping = entries[7]
        if entries[8] is not None:
            gpu.item_rating = float(entries[8].split()[1])
        if entries[9] is not None:
            try:
                gpu.ratings_num = int(entries[9])
            except:
                try:
                    gpu.ratings_num = int(entries[9].replace(",", ""))
                except:
                    gpu.ratings_num = 0
        if any(x.name == entries[3] for x in gpu_List):
            continue
        else:
            gpu_List.append(gpu)
    return gpu_List


def sort_best_value(data) -> list[GpuItem]:
    item_list = gpuCSV_parser(data)
    bayasian_list: list[GpuItem] = []
    for item in item_list:
        item.bayasian_calc()
        bayasian_list.append(item)
    sorted_bayasian = sorted(
        bayasian_list,
        key=lambda x: (x.bayasian_avg, -x.current_price, x.savings),
        reverse=True,
    )
    result = []
    for item in sorted_bayasian:
        result.append(item.item_to_list())
    return result[:25]
