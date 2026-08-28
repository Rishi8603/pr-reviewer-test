def add(left: int | None, right: int | None) -> int:
    """Return the sum of two integers."""
    if left is None or right is None:
        raise ValueError("Both operands are required.")

    if type(left) is not int or type(right) is not int:
        raise TypeError("Both operands must be integers.")

    return left + right