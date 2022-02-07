import decimal
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

_EASTER_HOLIDAY_BEGIN = date(2022, 4, 9)
_EASTER_HOLIDAY_END = date(2022, 4, 18)


def _truncate(t: Decimal) -> Decimal:
    return t.quantize(Decimal('0.01'), decimal.ROUND_DOWN)


def calculate_price(total: Decimal, day: date) -> Decimal:
    """Calculates the discounted price for the given total on the given day.

    If the given day is during the chocolatey Easter holidays, that is, between the 9th and the 18th of April 2022,
    a discount will be granted.
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

    if _EASTER_HOLIDAY_BEGIN <= day <= _EASTER_HOLIDAY_END:
        if total <= 50:
            discount = Decimal(0.95)
        elif total <= 100:
            discount = Decimal(0.9)
        else:
            discount = Decimal(0.85)

        discounted_total *= discount

    return discounted_total.quantize(Decimal('0.01'), ROUND_HALF_UP)
