"""Generate fake property data for the cloud function example"""

import datetime
import random
from dataclasses import dataclass, field

from faker import Faker
from faker.providers import BaseProvider

fake = Faker("en_GB")


@dataclass(init=False)
class Property(BaseProvider):
    """Property details generic to any property"""

    name: str = field()
    min_area: int = field()
    max_area: int = field()
    min_price: int = field()
    max_price: int = field()
    min_rooms: int = field()
    max_rooms: int = field()

    def address(self) -> str:
        """Create a property address"""
        return f"{fake.building_number()} {fake.street_name()}"

    def property_age(self, date_sold: str) -> int:
        """Age of property. Cannot be 'younger' than when it was last sold"""
        min_age: int = (
            datetime.datetime.today().year
            - datetime.datetime.strptime(date_sold, "%Y-%m-%d").year
        )
        max_age: int = min_age + 100
        return random.randint(min_age, max_age)

    def property_area(self) -> float:
        """Specify the area of the property"""
        return round(random.uniform(self.min_area, self.max_area), 2)

    def price_sold(self) -> float:
        """Specify the sale price of the property"""
        return round(random.uniform(self.min_price, self.max_price), 2)

    def total_rooms(self) -> int:
        """Specify the total number of rooms in the property"""
        return random.randint(self.min_rooms, self.max_rooms)

    def total_bedrooms(self, total_rooms: int) -> int:
        """Specify the total number of bedrooms in the property.
        Must be lower than the total number of rooms
        """
        max_bedrooms = max(1, total_rooms - 1)
        return random.randint(1, max_bedrooms)


@dataclass
class Flat(Property):
    """Flat specific property details"""

    name: str = "Flat"
    min_area: int = 100
    max_area: int = 1_000
    min_price: int = 70_000
    max_price: int = 500_000
    min_rooms: int = 1
    max_rooms: int = 5


@dataclass
class SemiDetachedHouse(Property):
    name: str = "Semi Detached"
    min_area: int = 1_000
    max_area: int = 2_000
    min_price: int = 150_000
    max_price: int = 900_000
    min_rooms: int = 5
    max_rooms: int = 10


@dataclass
class Bungalow(Property):
    name: str = "Bungalow"
    min_area: int = 600
    max_area: int = 1_500
    min_price: int = 70_000
    max_price: int = 400_000
    min_rooms: int = 3
    max_rooms: int = 6


@dataclass
class Maisonette(Property):
    name: str = "Maisonette"
    min_area: int = 1_000
    max_area: int = 1_500
    min_price: int = 100_000
    max_price: int = 900_000
    min_rooms: int = 4
    max_rooms: int = 9


@dataclass
class House(Property):
    name: str = "House"
    min_area: int = 1_500
    max_area: int = 4_000
    min_price: int = 70_000
    max_price: int = 1_500_000
    min_rooms: int = 5
    max_rooms: int = 15


@dataclass
class TerracedHouse(Property):
    name: str = "TerracedHouse"
    min_area: int = 900
    max_area: int = 2_000
    min_price: int = 70_000
    max_price: int = 500_000
    min_rooms: int = 5
    max_rooms: int = 9


@dataclass
class BadProperty(Property):
    """Property with unexepected data to potentially fail the validation tests"""

    name: str = random.choice(
        [
            "House",
            "TerracedHouse",
            "Maisonette",
            "Flat",
            "Semi Detached House",
            "Detached House",
            "Mansion",
            "Shopping Centre",
        ]
    )

    min_area: int = -1000
    max_area: int = 1000
    min_price: int = -100_000
    max_price: int = 100
    min_rooms: int = -100
    max_rooms: int = 1000
    chance: bool = random.uniform(0, 1) > 0.8

    def property_age(self, date_sold: str):
        """Age of property. Cannot be 'younger' than when it was last sold"""
        min_age: int = (
            datetime.datetime.today().year
            - datetime.datetime.strptime(date_sold, "%Y-%m-%d").year
        )
        max_age: int = min_age + 100
        if self.chance:
            # shouldn't be a string, will fail validation
            return str(random.randint(min_age, max_age))
        return random.randint(min_age, max_age)

    def property_area(self):
        """Specify the area of the property"""
        if self.chance:
            # way to big
            return self.max_area * 100_000
        return round(random.uniform(self.min_area, self.max_area), 2)

    def price_sold(self):
        """Specify the sale price of the property"""
        return round(random.uniform(self.min_price, self.max_price), 2)

    def total_rooms(self):
        """Specify the total number of rooms in the property"""
        if self.chance:
            # should return int
            return "nine"
        return random.randint(self.min_rooms, self.max_rooms)

    def total_bedrooms(self, total_rooms: int):
        """Specify the total number of bedrooms in the property.
        Must be lower than the total number of rooms
        """
        if self.chance:
            # should return int
            return "nine"
        max_bedrooms = max(1, total_rooms - 1)
        return random.randint(1, max_bedrooms)
