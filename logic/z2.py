def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n nie moze byc ujemne")

    first = 0
    second = 1

    for _ in range(n):
        first, second = second, first + second

    return first
