
import requests


class Brewery:
    def __init__(
        self,
        id: str,
        name: str,
        brewery_type: str,
        address_1: str | None = None,
        address_2: str | None = None,
        address_3: str | None = None,
        city: str | None = None,
        state_province: str | None = None,
        postal_code: str | None = None,
        country: str | None = None,
        longitude: float | None = None,
        latitude: float | None = None,
        phone: str | None = None,
        website_url: str | None = None,
        state: str | None = None,
        street: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.brewery_type = brewery_type
        self.address_1 = address_1
        self.address_2 = address_2
        self.address_3 = address_3
        self.city = city
        self.state_province = state_province
        self.postal_code = postal_code
        self.country = country
        self.longitude = longitude
        self.latitude = latitude
        self.phone = phone
        self.website_url = website_url
        self.state = state
        self.street = street

    def __str__(self) -> str:
        return f"({self.id},{self.name},{self.brewery_type},{self.address_1},{self.address_2},{self.address_3},{self.city},{self.state_province},{self.postal_code},{self.country},{self.longitude},{self.latitude},{self.phone},{self.website_url},{self.state},{self.street})"

def run() -> None:
    url = "https://api.openbrewerydb.org/v1/breweries"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    breweries: list[Brewery] = []

    for brew in data:
        brewery = Brewery(
            id=brew["id"],
            name=brew["name"],
            brewery_type=brew["brewery_type"],
            address_1=brew.get("address_1"),
            address_2=brew.get("address_2"),
            address_3=brew.get("address_3"),
            city=brew.get("city"),
            state_province=brew.get("state_province"),
            postal_code=brew.get("postal_code"),
            country=brew.get("country"),
            longitude=brew.get("longitude"),
            latitude=brew.get("latitude"),
            phone=brew.get("phone"),
            website_url=brew.get("website_url"),
            state=brew.get("state"),
            street=brew.get("street"),
        )

        breweries.append(brewery)

    for brewery in breweries[:20]:
        print(brewery)


if __name__ == "__main__":
    run()
