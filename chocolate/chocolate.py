import decimal
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

_WINTER_SEASON_BEGIN = date(2023, 11, 25)
_WINTER_SEASON_END = date(2024, 1, 6)


def _truncate(t: Decimal) -> Decimal:
    return t.quantize(Decimal('0.01'), decimal.ROUND_DOWN)


def calculate_price(total: Decimal, day: date) -> Decimal:
    """Calculates the discounted price for the given total on the given day.

    If the given day is during the chocolatey Winter season, that is, between the 25th of November 2023
    and the 6th of January 2024, a discount will be granted.
    :param:
    :return: The discounted total
    """
    if not isinstance(total, Decimal):
        raise ValueError("Given total must be of type Decimal.")
    if total < 0:
        raise ValueError("Given total must be positive or zero")
    if not isinstance(day, date):
        raise ValueError("Given day must be of type date")

    if total.as_tuple().exponent < -2:
        print(f"Warning: The given total {total} has more than two decimal places. Decimal places will be"
              f" truncated, calculations will be based on the truncated value {_truncate(total)}.")

    discounted_total = _truncate(total)

    if _WINTER_SEASON_BEGIN <= day <= _WINTER_SEASON_END:
        if total <= 50:
            discount = Decimal(0.95)
        elif total <= 100:
            discount = Decimal(0.9)
        else:
            discount = Decimal(0.85)

        discounted_total *= discount

    return discounted_total.quantize(Decimal('0.01'), ROUND_HALF_UP)
