import decimal
import re
from enum import Enum
from decimal import Decimal
from datetime import date


class Rating(Enum):
    FIRST_TIME = "First time"
    REGULAR = "Regular"
    SUPER_DUPER = "Super-duper"

    def __str__(self):
        return self.name


class Customer:
    def __init__(self, name: str, rating: Rating):
        if not isinstance(name, str):
            raise ValueError(f"Customer name must be a string.")
        if len(name) == 0:
            raise ValueError(f"Customer name must be non-empty.")
        if not isinstance(rating, Rating):
            raise ValueError(f"Customer rating must be of type Rating, but is of type {type(rating)}.")

        self.name = name
        self.rating = rating

    def __str__(self):
        return f"{self.name} ({self.rating})"


class Product:
    _EAN_PATTERN = re.compile(r"^\d{13}$")

    _RATING_TO_DISCOUNT = {
        Rating.FIRST_TIME: Decimal("0.05"),
        Rating.REGULAR: Decimal("0.1"),
        Rating.SUPER_DUPER: Decimal("0.15")
    }

    def __init__(self, ean: str, name: str, description: str, base_price: Decimal, base_discount=Decimal(0)):
        if not Product._EAN_PATTERN.match(ean):
            raise ValueError(f"Given ean {ean} is not valid. An ean has exactly 13 digits.")
        if not isinstance(name, str):
            raise ValueError(f"Product name must be a string.")
        if len(name) == 0:
            raise ValueError(f"Product name must be non-empty.")
        if not (isinstance(description, str) or description is None):
            raise ValueError(f"Product description must be a string or None, but is '{description}'")
        if not isinstance(base_price, Decimal):
            raise ValueError(f"Product base price must be of type Decimal.")
        if not base_price >= 0:
            raise ValueError(f"Product base price must be greater or equal to zero.")
        if not isinstance(base_discount, Decimal):
            raise ValueError(f"Product discount must be of type Decimal.")
        if base_discount < 0 or base_discount > 1:
            raise ValueError(f"Product discount must be between 0 and 1.")

        self.ean = ean
        self.name = name
        self.description = description
        self.base_price = base_price
        self.base_discount = base_discount

    @staticmethod
    def _is_within_summer_sale_period(d: date) -> bool:
        return d.month in (7, 8) and d.year == 2024

    @staticmethod
    def _is_friday_or_saturday(d: date) -> bool:
        return d.isoweekday() in (5, 6)

    def calculate_price_for_customer(self, customer: Customer, date_of_purchase: date) -> Decimal:
        if not isinstance(customer, Customer):
            raise ValueError("Given customer is not of type Customer, but is of " + str(type(customer)))
        if not isinstance(date_of_purchase, date):
            raise ValueError("Given date_of_purchase is not of type date, but is a " + str(type(date_of_purchase)))

        discount = Decimal(0)

        if Product._is_within_summer_sale_period(date_of_purchase):
            discount = Product._RATING_TO_DISCOUNT.get(customer.rating)

        if Product._is_friday_or_saturday(date_of_purchase):
            discount = discount * 2

        # Apply the two discounts
        price = self.base_price * (Decimal(1) - self.base_discount) * (Decimal(1) - discount)

        # Round to two digits precision
        price = price.quantize(Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)

        return price

