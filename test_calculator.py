from calculator import add


def test_add_returns_sum() -> None:
    assert add(2, 3) == 5


def test_add_handles_zero_values() -> None:
    assert add(0, 5) == 5
    assert add(0, 0) == 0


def test_add_handles_negative_left_operand() -> None:
    assert add(-2, 3) == 1


def test_add_handles_negative_right_operand() -> None:
    assert add(2, -3) == -1


def test_add_handles_two_negative_operands() -> None:
    assert add(-2, -3) == -5
