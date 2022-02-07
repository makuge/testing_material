import pytest
from decimal import Decimal
from datetime import date
from chocolate import calculate_price


_test_data_during_easter_holidays = [
    pytest.param(Decimal('0'), date(2022, 4, 9), Decimal('0'), id="3 - 0 on first day"),
    pytest.param(Decimal('0'), date(2022, 4, 18), Decimal('0'), id="11 - 0 on last day"),
    pytest.param(Decimal('0.01'), date(2022, 4, 9), Decimal('0.01'), id="4 - Very small total (0.01) on first day"),
    pytest.param(Decimal('0.01'), date(2022, 4, 18), Decimal('0.01'), id="12 - Very small total (0.01) on last day"),
    pytest.param(Decimal('49.99'), date(2022, 4, 9), Decimal('47.49')),
    pytest.param(Decimal('49.99'), date(2022, 4, 18), Decimal('47.49')),
    pytest.param(Decimal('50'), date(2022, 4, 9), Decimal('47.5')),
    pytest.param(Decimal('50'), date(2022, 4, 18), Decimal('47.5')),
    pytest.param(Decimal('50.01'), date(2022, 4, 9), Decimal('45.01')),
    pytest.param(Decimal('50.01'), date(2022, 4, 18), Decimal('45.01')),
    pytest.param(Decimal('99.99'), date(2022, 4, 9), Decimal('89.99')),
    pytest.param(Decimal('99.99'), date(2022, 4, 18), Decimal('89.99')),
    pytest.param(Decimal('100'), date(2022, 4, 9), Decimal('90')),
    pytest.param(Decimal('100'), date(2022, 4, 18), Decimal('90')),
    pytest.param(Decimal('100.01'), date(2022, 4, 9), Decimal('85.01')),
    pytest.param(Decimal('100.01'), date(2022, 4, 18), Decimal('85.01'))
]


@pytest.mark.parametrize("total,day,expected", _test_data_during_easter_holidays)
def test_prices_during_easter_holidays(total: Decimal, day: date, expected: Decimal):
    # Act
    actual = calculate_price(total, day)
    # Assert
    assert actual == expected


_test_data_outside_easter_holidays = [
    pytest.param(Decimal('50'), date(2022, 2, 2), Decimal('50'), id="1 - No discount two months before easter holidays"),
    pytest.param(Decimal('50'), date(2022, 4, 8), Decimal('50'), id="2 - No discount one day before easter holidays"),
    pytest.param(Decimal('100'), date(2022, 4, 19), Decimal('100'), id="19 - No discount one day after easter holidays"),
    pytest.param(Decimal('100'), date(2022, 10, 28), Decimal('100'), id="20 - No discount in October")
]


@pytest.mark.parametrize("total,day,expected", _test_data_outside_easter_holidays)
def test_prices_outside_easter_holiday(total: Decimal, day: date, expected: Decimal):
    actual = calculate_price(total, day)
    assert actual == expected


_invalid_test_data = [
    pytest.param(100.0, date(2022, 4, 9), id="21 - total not a Decimal"),
    pytest.param(Decimal('-93.2'), date(2022, 4, 9), id="22 - total negative"),
    pytest.param(Decimal('50'), True, id="23 - day not a date")
]


@pytest.mark.parametrize("total,day", _invalid_test_data)
def test_invalid_arguments(total: Decimal, day: date):
    with pytest.raises(ValueError):
        calculate_price(total, day)

