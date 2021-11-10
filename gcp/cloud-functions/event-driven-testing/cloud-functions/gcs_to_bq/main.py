"""Move data from GCS to BigQuery"""
import logging
import os
from typing import Optional

from src.bq_loaders import (
    AvroBigQueryLoader,
    BigQueryLoader,
    CsvBigQueryLoader,
    NewLineJsonBigQueryLoader,
    ParquetBigQueryLoader,
)

PROJECT = os.environ["PROJECT"]
BUCKET = os.environ["BUCKET"]
VALIDATION_BUCKET = os.environ["VALIDATION_BUCKET"]

extension_mapping = {
    "csv": CsvBigQueryLoader,
    "parquet": ParquetBigQueryLoader,
    "avro": AvroBigQueryLoader,
    "json": NewLineJsonBigQueryLoader,
}


def extract_file_extension(file_name: str) -> str:
    """Extract the file extension from the file path"""
    return file_name.split(".")[-1]


def batch_load_bq(data, context):  # pylint: disable=unused-argument
    """Batch load from GCS to Bigquery"""

    file_extension = extract_file_extension(data["name"])
    loader: Optional[BigQueryLoader] = extension_mapping.get(file_extension)

    if loader:
        # TODO: remove hard coded properties reference
        loader = loader(
            project=PROJECT,
            file_name=data["name"],
            data_bucket=BUCKET,
            validation_bucket=VALIDATION_BUCKET,
            bq_dataset="test_dataset",
            bq_table="properties",
            config_path="config/properties/bq_load.json",
        )

        loader.load_config()
        loader.load()

        logging.info("Job finished")

    else:
        raise ValueError(f"File extension {file_extension} is not supported")

    # destination_table = client.get_table(dataset_ref.table(TABLE))
    # logging.info("Loaded {} rows.".format(destination_table.num_rows))
