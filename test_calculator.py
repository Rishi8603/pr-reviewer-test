import pytest

from calculator import add


def test_add_returns_sum() -> None:
    assert add(2, 3) == 5


def test_add_accepts_zero() -> None:
    assert add(0, 5) == 5


def test_add_accepts_negative_numbers() -> None:
    assert add(-2, 3) == 1


def test_add_rejects_missing_left_operand() -> None:
    with pytest.raises(ValueError):
        add(None, 3)


def test_add_rejects_missing_right_operand() -> None:
    with pytest.raises(ValueError):
        add(3, None)


def test_add_rejects_float_left_operand() -> None:
    with pytest.raises(TypeError):
        add(1.5, 2)


def test_add_rejects_float_right_operand() -> None:
    with pytest.raises(TypeError):
        add(2, 1.5)


def test_add_rejects_boolean_operand() -> None:
    with pytest.raises(TypeError):
        add(True, 2)