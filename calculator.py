def add(left: int | None, right: int | None) -> int:
    """Return the sum of two integers."""
    if left is None or right is None:
        raise ValueError("Both operands are required.")

    return left + right