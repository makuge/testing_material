def calculate_discount(amount: int, member: bool) -> float:
    """
    Calculates the discount for a purchase of juice depending on the amount a customer purchases and whether she is a
    bonus club member.
    :param amount: The amount of juice cartons the customer purchases
    :param member: Whether the customer is a bonus club member
    :return: The discount between 0 and 1
    :raises:
        ValueError: if amount is not an integer or not within the accepted range, e.g., 0 < amount <= 10
    """

    if not isinstance(amount, int):
        raise ValueError("amount must be an int")
    if amount < 1 or amount > 10:
        raise ValueError("amount has to be greater than 0 and less or equal to 10")

    percentages = {(1, 2): 1.0, (3, 3): 3 / 4, (4, 5): 2 / 3, (6, 10): 1 / 2}

    for interval, percentage in percentages.items():
        if interval[0] <= amount <= interval[1]:
            if member:
                percentage *= 4 / 5

            return 1 - percentage

    raise RuntimeError("Logical error. Check implementation.")
