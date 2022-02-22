import decimal
from decimal import Decimal
from datetime import date

_holidays = (date(2022, 12, 8), date(2022, 12, 25), date(2022, 12, 26))

_1st_advent_saturday = date(2022, 11, 26)
_christmas = date(2022, 12, 24)


def _truncate(t: Decimal) -> Decimal:
    return t.quantize(Decimal('0.01'), decimal.ROUND_DOWN)


def calculate_discount(day: date, total: Decimal) -> Decimal:
    if not isinstance(day, date):
        raise ValueError("Given date must be of type date")
    if (_1st_advent_saturday <= day <= _christmas and day.weekday() == 6) or day in _holidays:
        raise ValueError("Discounts not calculable on sundays and holidays.")

    if not isinstance(total, Decimal):
        raise ValueError("Given sum must be of type Decimal")
    if total <= 0:
        raise ValueError("Given total must be greater or equal to 0")

    is_in_advent = _1st_advent_saturday <= day <= _christmas
    is_discount_day = (is_in_advent and day.weekday() == 5) or day == _christmas

    percentages = {(0, 100): Decimal(95) / Decimal(100),
                   (100, 500): Decimal(9) / Decimal(10),
                   (500, Decimal('Infinity')): Decimal(8) / Decimal(10)}

    if total.as_tuple().exponent < -2:
        print(f"Warning: The given total {total} has more than two decimal places. Decimal places will be"
              f" truncated, calculations will be based on the truncated value {_truncate(total)}.")

    rounded_total = _truncate(total)

    percentage = Decimal(1)

    if is_in_advent:
        for interval, interval_percentage in percentages.items():
            if interval[0] <= rounded_total < interval[1]:
                percentage = interval_percentage
                break

    if is_discount_day:
        percentage *= Decimal(9) / Decimal(10)

    discount = Decimal(1) - percentage

    return discount.quantize(Decimal('0.01'), decimal.ROUND_HALF_UP)

