def count_vowels(text: str) -> int:
    vowels = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
    count = 0
    for char in text.lower():
        if char.lower() in vowels:
            count += 1
    return count
