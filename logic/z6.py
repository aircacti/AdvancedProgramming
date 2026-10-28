import string


def word_frequencies(text: str) -> dict:
    counter = {}

    b = text.translate(str.maketrans('', '', string.punctuation))
    for c in b.lower().split():
        if c in counter:
            counter[c] += 1
        else:
            counter[c] = 1

    return counter
