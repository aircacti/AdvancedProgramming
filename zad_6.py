

def doThing(a: list, b: list) -> list:
    combined = a.copy()

    for x in b:
        if x not in combined:
            combined.append(x)

    powered = []
    for x in combined:
        powered.append(x ** 3)

    return powered

a = [1,2,3]
b = [2,4]
print(doThing(a,b))