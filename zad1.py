# Stworzyć klasę Student, która posiada 2 parametry (name i marks) oraz jedną metodę is_passed,
# która zwraca wartość logiczną, pozytywną gdy średnia ocen jest > 50 w przeciwnym przypadku negatywną.
# Następnie należy stworzyć 2 przykładowe obiekty klasy, tak aby
# dla pierwszego obiektu metoda zwracała true , a dla drugiego false.

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def is_passed(self):
        return sum(self.marks) / len(self.marks) > 50

St1 = Student("John", [100, 90, 80, 75])
St2 = Student("Olaf", [0, 35, 49, 50])
print(f"{St1.name}: oceny {St1.marks} Zdał? = {St1.is_passed()}")
print(f"{St2.name}: oceny {St2.marks} Zdał? = {St2.is_passed()}")


