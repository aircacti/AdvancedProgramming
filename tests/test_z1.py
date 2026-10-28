from logic.z1 import is_palindrome


def test_palindrome1():
    assert is_palindrome("kajak") is True


def test_palindrome2():
    assert is_palindrome("Kobyła ma mały bok") is True


def test_palindrome3():
    assert is_palindrome("python") is False


def test_palindrome4():
    assert is_palindrome("") is True


def test_palindrome5():
    assert is_palindrome("A") is True
