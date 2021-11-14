"""Generate fake property data for the cloud function example"""

import csv
import datetime
import logging
import os
import random
from typing import List

from faker import Faker
from properties import (
    Bungalow,
    Flat,
    House,
    Maisonette,
    Property,
    SemiDetachedHouse,
    TerracedHouse,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def create_dir_to_save_data(save_dir_location: str):
    """Create a folder to save the data if it doesn't already exist"""
    if not os.path.exists(save_dir_location):
        os.makedirs(save_dir_location)


def generate_batch_data(
    property_choices: List,
    dataset_name: str,
    col_headers: List[str],
    data_dir: str,
    num_records: int,
):
    """Generate batch csv data

    Args:
        property_choices (List): list of available property types which are
            subclasses of Property
        dataset_name (str): name of the dataset e.g. properties
        col_headers (List[str]): list of column names
        data_dir (str): relative location of the data directory to this script
        num_records (int): number of fake rows of data to generate

    Returns:
        saves a csv file in the `data_dir/dataset_name` directory containing the
        fake data


    """
    logger.info(
        (
            f"Starting data generation for {dataset_name} dataset "
            f"with {num_records:,} records"
        )
    )

    save_dir_location = f"{data_dir}/{dataset_name}"
    create_dir_to_save_data(save_dir_location)

    timestamp_str = datetime.datetime.now().strftime("%d%m%Y-%H:%M:%S")
    filename = f"{save_dir_location}/{dataset_name}_{timestamp_str}.csv"

    fake = Faker("en_GB")
    fake.add_provider(Property)

    with open(filename, "w") as data_dump:
        writer = csv.DictWriter(
            data_dump, fieldnames=col_headers, delimiter=",", quoting=csv.QUOTE_ALL
        )

        for i in range(num_records):

            property_type = random.choice(property_choices)
            fake.add_provider(property_type)

            property_id = i
            property_type = property_type.name
            address = fake.address()
            city = fake.city()
            county = fake.county()
            post_code = fake.postcode()
            date_sold = fake.date_between().strftime("%Y-%m-%d")
            property_age = fake.property_age(date_sold)
            total_rooms = fake.total_rooms()
            total_bedrooms = fake.total_bedrooms(total_rooms)
            property_area = fake.property_area()
            price_sold = fake.price_sold()

            row = {
                "propertyId": property_id,
                "address": address,
                "city": city,
                "county": county,
                "postCode": post_code,
                "propertyType": property_type,
                "dateSold": date_sold,
                "propertyAge": property_age,
                "totalRooms": total_rooms,
                "totalBedrooms": total_bedrooms,
                "propertyArea": property_area,
                "priceSold": price_sold,
            }

            writer.writerow(row)
            if i % 10_000 == 0:
                logger.info(f"{i:,}/{num_records:,} records generated")


if __name__ == "__main__":
    property_choices = [
        Flat,
        SemiDetachedHouse,
        Bungalow,
        Maisonette,
        House,
        TerracedHouse,
    ]

    dataset_name = "properties"
    col_headers = [
        "propertyId",
        "address",
        "city",
        "county",
        "postCode",
        "propertyType",
        "dateSold",
        "propertyAge",
        "totalRooms",
        "totalBedrooms",
        "propertyArea",
        "priceSold",
    ]
    data_dir = "../data"
    num_records = 100_000

    generate_batch_data(
        property_choices=property_choices,
        dataset_name=dataset_name,
        col_headers=col_headers,
        data_dir=data_dir,
        num_records=num_records,
    )
