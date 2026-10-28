import pytest

from logic.z2 import fibonacci


def test_fibonacci1():
    assert fibonacci(0) is 0


def test_fibonacci2():
    assert fibonacci(1) is 1


def test_fibonacci3():
    assert fibonacci(5) is 5


def test_fibonacci4():
    assert fibonacci(10) is 55


def test_fibonacci5():
    with pytest.raises(ValueError):
        fibonacci(-1)
