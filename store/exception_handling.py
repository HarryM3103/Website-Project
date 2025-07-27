def rawHTML_Handling(container) -> list[str]:
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
    return data_entries
