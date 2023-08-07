class GpuItem:
    def __init__(
        self,
        image: str = None,
        brand: str = None,
        link: str = None,
        name: str = None,
        current_price: float = 0,
        previous_price: float = None,
        savings: int = 0,
        shipping: str = None,
        item_rating: float = None,
        ratings_num: int = None,
    ) -> None:
        self.image = image
        self.brand = brand
        self.link = link
        self.name = name
        self.current_price = current_price
        self.previous_price = previous_price
        self.savings = savings
        self.shipping = shipping
        self.item_rating = item_rating
        self.ratings_num = ratings_num
        self.bayasian_avg = None

    def bayasian_calc(self) -> float:
        if (self.item_rating == None) or (self.ratings_num == None):
            self.item_rating = 3
            self.ratings_num = 1
        new_ratings = 2 + self.ratings_num
        self.bayasian_avg = ((self.item_rating * self.ratings_num) + 4) / new_ratings

    def item_to_list(self):
        string_list = []
        try:
            string_list.append(self.image)
        except:
            string_list.append("None")

        try:
            string_list.append(self.brand)
        except:
            string_list.append("None")

        try:
            string_list.append(self.link)
        except:
            string_list.append("None")

        try:
            string_list.append(self.name)
        except:
            string_list.append("None")

        try:
            string_list.append(str(self.current_price))
        except:
            string_list.append("None")

        try:
            string_list.append(str(self.previous_price))
        except:
            string_list.append("None")

        try:
            string_list.append(str(self.savings))
        except:
            string_list.append("None")

        try:
            string_list.append(self.shipping)
        except:
            string_list.append("None")

        try:
            string_list.append(str(self.item_rating))
        except:
            string_list.append("None")

        try:
            string_list.append(str(self.ratings_num))
        except:
            string_list.append("None")

        return string_list
