class Property:
    def __init__(self, area, rooms: int, price, address):
        self.area = area
        self.rooms = rooms
        self.price = price
        self.address = address

    def __str__(self):
        return (f"Property({self.area},"
                f"{self.rooms},{self.price},{self.address})")


class House(Property):
    def __init__(self, plot: int, area, rooms, price, address):
        super().__init__(area, rooms, price, address)
        self.plot = plot

    def __str__(self):
        return f"House({self.plot}) of {super().__str__()}"


class Flat(Property):
    def __init__(self, floor: int, area, rooms, price, address):
        super().__init__(area, rooms, price, address)
        self.floor = floor

    def __str__(self):
        return f"Flat({self.floor}) of {super().__str__()}"
