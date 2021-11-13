"""Generate fake property data for the cloud function example"""


import csv
import datetime
import os
import random
from itertools import count
from typing import List

from faker import Faker
from faker.providers import BaseProvider

fake = Faker("en_GB")


class PropertyDetails(BaseProvider):

    PROPERTY_TYPES = [
        "Flat",
        "Maisonette",
        "Bungalow",
        "House",
        "Terraced House",
        "Semi Detached House",
    ]

    id_counter = count()

    def property_id(self):
        """Define a sequential id for the property"""
        return next(self.id_counter)

    def property_type(self) -> str:
        """Choose a random property type"""
        return random.choice(self.PROPERTY_TYPES)

    def address(self) -> str:
        return f"{fake.build_number()} {fake.street_name}"

    def town(self) -> str:
        return fake.city()

    def county(self) -> str:
        return fake.county()

    def postcode(self) -> str:
        return fake.postcode()

    def property_age(self) -> int:
        return random.randint(0, 70)

    def property_area(self, property_type):
        """Define property area (sqft)"""
        if property_type == "Studio":
            return round(random.uniform(29.99, 50.99))
        elif property_type in ("Flat", "Maisonette", "Bungalow"):
            return round(random.uniform(50.99, 150.99))
        else:
            return round(random.uniform(100.99, 250.99))

    def price_sold(self, property_type):
        if property_type == "Studio":
            return round(random.uniform(40000, 250000))
        elif property_type in ("Flat", "Maisonette", "Bungalow"):
            return round(random.uniform(70000, 350000))
        else:
            return round(random.uniform(110000, 999999))

    def total_rooms(self, property_type):
        """Total rooms in the property"""
        if property_type == "Studio":
            return 1
        elif property_type in ("Flat", "Maisonette", "Bungalow", "Terraced House"):
            return random.randint(2, 5)
        else:
            return random.randint(4, 7)

    def total_bedrooms(self, property_type, total_rooms):
        """Total bedrooms should be less than total number of rooms"""
        if property_type == "Studio":
            return 1
        elif property_type in ("Flat", "Maisonette", "Bungalow", "Terraced House"):
            if total_rooms > 2:
                return total_rooms - 1
            else:
                return total_rooms
        else:
            if total_rooms > 3:
                return total_rooms - 2
            else:
                return total_rooms - 1


def generate_batch_data(
    faker_provider: BaseProvider,
    dataset_name: str,
    col_headers: List[str],
    data_dir: str,
    num_records: int,
):
    """Generate batch csv data"""
    save_dir_location = f"{data_dir}/{dataset_name}"

    if not os.path.exists(save_dir_location):
        os.makedirs(save_dir_location)

    timestamp_str = datetime.datetime.now().strftime("%d%m%Y-%H:%M:%S")
    filename = f"{save_dir_location}/{timestamp_str}.csv"

    fake.add_provider(faker_provider)

    with open(filename, "w") as data_dump:
        writer = csv.DictWriter(
            data_dump, fieldnames=col_headers, delimiter=",", quoting=csv.QUOTE_ALL
        )

        for _ in range(num_records):
            property_type = fake.property_type()
            property_area = fake.property_area(property_type)
            price_sold = fake.price_sold(property_type)
            total_rooms = fake.total_rooms(property_type)
            total_bedrooms = fake.total_bedrooms(property_type, total_rooms)
            date_sold = fake.date_between(
                start_date=datetime.date(1850, 1, 1)
            ).strftime("%Y-%m-%d")

            row = {
                "propertyId": fake.property_id(),
                "customerId": fake.random_int(1, 501_000),
                "address": fake.address,
                "town": fake.city,
                "county": fake.county,
                "postCode": fake.postcode,
                "propertyAge": fake.property_age,
                "propertyType": property_type,
                "totalRooms": total_rooms,
                "totalBedrooms": total_bedrooms,
                "propertyArea": property_area,
                "priceSold": price_sold,
                "dateSold": date_sold,
            }

            writer.writerow(row)
