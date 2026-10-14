
def checkNumberEven(num) -> bool:
    return num % 2 == 0


res = checkNumberEven(4)
if res:
    print("Liczba parzysta")
else:
    print("Liczba nieparzysta")