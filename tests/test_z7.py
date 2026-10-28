from logic.z7 import is_prime


def test_prime1():
    assert is_prime(2) is True


def test_prime2():
    assert is_prime(3) is True


def test_prime3():
    assert is_prime(4) is False


def test_prime4():
    assert is_prime(0) is False


def test_prime5():
    assert is_prime(1) is False


def test_prime6():
    assert is_prime(5) is True


def test_prime7():
    assert is_prime(97) is True
