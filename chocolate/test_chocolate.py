import pytest
from decimal import Decimal
from datetime import date
from chocolate import calculate_price
#from chocolate_dummy import calculate_price


_test_data_during_easter_holidays = [
    pytest.param(Decimal('0'), date(2023, 11, 25), Decimal('0'), id="3 - 0 on first day"),
    pytest.param(Decimal('0'), date(2024, 1, 6), Decimal('0'), id="11 - 0 on last day"),
    pytest.param(Decimal('0.01'), date(2023, 11, 25), Decimal('0.01'), id="4 - Very small total (0.01) on first day"),
    pytest.param(Decimal('0.01'), date(2024, 1, 6), Decimal('0.01'), id="12 - Very small total (0.01) on last day"),
    pytest.param(Decimal('49.99'), date(2023, 12, 9), Decimal('47.49')),
    pytest.param(Decimal('49.99'), date(2024, 1, 2), Decimal('47.49')),
    pytest.param(Decimal('50'), date(2023, 12, 9), Decimal('47.5')),
    pytest.param(Decimal('50'), date(2024, 1, 2), Decimal('47.5')),
    pytest.param(Decimal('50.01'), date(2023, 12, 9), Decimal('45.01')),
    pytest.param(Decimal('50.01'), date(2024, 1, 2), Decimal('45.01')),
    pytest.param(Decimal('99.99'), date(2023, 12, 9), Decimal('89.99')),
    pytest.param(Decimal('99.99'), date(2024, 1, 2), Decimal('89.99')),
    pytest.param(Decimal('100'), date(2023, 12, 9), Decimal('90')),
    pytest.param(Decimal('100'), date(2024, 1, 2), Decimal('90')),
    pytest.param(Decimal('100.01'), date(2023, 12, 9), Decimal('85.01')),
    pytest.param(Decimal('100.01'), date(2024, 1, 2), Decimal('85.01'))
]


@pytest.mark.parametrize("total,day,expected", _test_data_during_easter_holidays)
def test_prices_during_easter_holidays(total: Decimal, day: date, expected: Decimal):
    # Act
    actual = calculate_price(total, day)
    # Assert
    assert actual == expected


_test_data_outside_winter_season = [
    pytest.param(Decimal('50'), date(2023, 9, 23), Decimal('50'),
                 id="1 - No discount in September 2023"),
    pytest.param(Decimal('50'), date(2023, 11, 24), Decimal('50'),
                 id="2 - No discount one day before the winter season begin"),
    pytest.param(Decimal('100'), date(2024, 1, 7), Decimal('100'),
                 id="19 - No discount one day after the winter season end"),
    pytest.param(Decimal('100'), date(2024, 3, 6), Decimal('100'),
                 id="20 - No discount in March 2024")
]


@pytest.mark.parametrize("total,day,expected", _test_data_outside_winter_season)
def test_prices_outside_easter_holiday(total: Decimal, day: date, expected: Decimal):
    actual = calculate_price(total, day)
    assert actual == expected


_invalid_test_data = [
    pytest.param(100.0, date(2023, 12, 9), id="21 - total not a Decimal"),
    pytest.param(Decimal('-93.2'), date(2024, 1, 1), id="22 - total negative"),
    pytest.param(Decimal('50'), True, id="23 - day not a date")
]


@pytest.mark.parametrize("total,day", _invalid_test_data)
def test_invalid_arguments(total: Decimal, day: date):
    with pytest.raises(ValueError):
        calculate_price(total, day)


# import itertools
# combinations = list(itertools.product(
#    list(map(Decimal, '0 0.01 49.99 50 50.01 99.99 100 100.01'.split())),
#    [date(2022, 4, 9), date(2022, 4, 18)]))

# for idx, combination in enumerate(combinations):
#    print(f"pytest.param({combination}),")
