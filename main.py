import magazine.Product
from obiektowosc.Student import Student
from obiektowosc.Housing import House as OHouse
from obiektowosc.Housing import Flat as OFlat


if __name__ == "__main__":
    St1 = Student("John", [100, 90, 80, 75])
    St2 = Student("Olaf", [0, 35, 49, 50])
    print(f"{St1.name}: oceny {St1.marks} Zdał? = {St1.is_passed()}")
    print(f"{St2.name}: oceny {St2.marks} Zdał? = {St2.is_passed()}")

    house1 = OHouse(200, "90m2", 7, 1000000, "ul. Wiejska 1 Warszawa")
    flat1 = OFlat(8, "50m2", 4, 500000, "ul. Marszałkowska 3 Warszawa")

    print(house1)
    print(flat1)
