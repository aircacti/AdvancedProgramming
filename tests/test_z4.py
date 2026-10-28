import pytest

from logic.z4 import calculate_discount


def test_calculate_discount1():
    assert (calculate_discount(100, 0.2) == 80.0)


def test_calculate_discount2():
    assert (calculate_discount(50, 0) == 50.0)


def test_calculate_discount3():
    assert (calculate_discount(200, 1) == 0.0)


def test_calculate_discount4():
    with pytest.raises(ValueError):
        calculate_discount(100, -0.1)


def test_calculate_discount5():
    with pytest.raises(ValueError):
        calculate_discount(100, 1.5)
