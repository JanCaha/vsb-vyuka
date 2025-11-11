import pytest


def test_ukazka():
    result = 1 + 2
    assert result == 3


def test_ukazka_1():
    result = 2 + 2
    assert result == 4


def test_ukazka_2():
    result = 2.5 + 1
    assert result == 3.5
    assert isinstance(result, float)


def test_ukazka_3():
    result = 0.1 + 0.1 + 0.1
    assert result == pytest.approx(0.3, abs=1e-6)
    assert isinstance(result, float)
