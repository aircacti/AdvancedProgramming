from logic.z3 import count_vowels


def test_cvovewls1():
    assert count_vowels("Python") == 2


def test_cvovewls2():
    assert count_vowels("AEIOUY") == 6


def test_cvovewls3():
    assert count_vowels("bcd") == 0


def test_cvovewls4():
    assert count_vowels("") == 0


def test_cvovewls5():
    assert count_vowels("Próba żółwia") == 5  # Zmiana w stosunku do notion
