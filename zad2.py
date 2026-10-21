class Library:
    def __init__(self, city, street, zip_code, open_hours, phone):
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hours = open_hours
        self.phone = phone

    def __str__(self):
        return f"{self.city} {self.street} {self.zip_code} {self.open_hours} {self.phone}"


class Employee:
    def __init__(self , first_name, last_name, hire_date, birth_date, city, street, zip_code, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone = phone

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.hire_date} {self.birth_date} {self.city} {self.street} {self.zip_code} {self.phone}"

class Book:
    def __init__(self, library, publication_date, author_name, author_surname, number_of_pages):
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages

    def __str__(self):
        return f"{self.library} {self.publication_date} {self.author_name} {self.author_surname} {self.number_of_pages}"

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def is_passed(self):
        return sum(self.marks) / len(self.marks) > 50

    def __str__(self):
        return f"{self.name} {self.marks}"

class Order:
    def __init__(self, employee, student, books, order_date):
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self):

        bt = ", ".join(str(b) for b in self.books)

        # Celowo mniej info żeby było czytelniej
        return f"({self.employee.first_name} {self.employee.last_name} przyjął zamówienie od {self.student.name} na książki: [{bt} {self.order_date})]"


if __name__ == '__main__':
    lib1 = Library('Amsterdam', 'IdkStreet', '12-667', '8-15', '123123123')
    lib = Library('Kraków', 'Mariacka', '30-100', '6-9', '873452768')

    book1 = Book(lib1, '1.1.2000', 'Jan', 'Kowalski', 67)
    book2 = Book(lib1, '2.1.1900', 'Mariusz', 'Kowalski', 60)
    book3 = Book(lib1, '2.8.1700', 'Mateusz', 'Kowalski', 60)
    book4 = Book(lib1, '8.8.1700', 'Mateusz', 'Nowak', 50)
    book5 = Book(lib1, '4.3.2025', 'Christopher', 'Nolan', 2000)

    emp1 = Employee('Jan', 'Nowak', '1.6.2025', '1.1.2000', 'Wrocław', 'Makapaki', '70-220', '898765678')
    emp2 = Employee('Mateusz', 'Nowak', '1.6.2025', '1.1.2000', 'Wrocław', 'Makapaki', '70-220', '898765678')
    emp3 = Employee('Grzegorz', 'Nowak', '1.6.2025', '1.1.2000', 'Wrocław', 'Makapaki', '70-220', '898765678')

    stud1 = Student('Patryk Vega', [0, 0, 0])
    stud2 = Student('Krystian Orzechowski', [70, 80, 99])
    stud3 = Student('Krystian Wacławczyk', [70, 80, 99])

    order1 = Order(emp2, stud1, [book5, book2], '21.10.2026')
    order2 = Order(emp3, stud2, [book1, book4], '19.8.2025')

    print(order1)
    print(order2)

