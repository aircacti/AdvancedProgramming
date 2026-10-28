def calculate_discount(price: float, discount: float) -> float:
    if discount < 0 or discount > 1:
        raise ValueError("discount musi być w zakresie od 0 do 1")

    return price - (price * discount)
