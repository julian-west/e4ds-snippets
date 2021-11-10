"""Move data from GCS to BigQuery"""
import logging
import os

from google.cloud import bigquery, storage
from src.bq_loaders import BigQueryLoader

PROJECT = os.environ["PROJECT"]
BUCKET = os.environ["BUCKET"]
VALIDATION_BUCKET = os.environ["VALIDATION_BUCKET"]

extension_mapping = {
    "csv": bigquery.SourceFormat.CSV,
    "avro": bigquery.SourceFormat.AVRO,
    "parquet": bigquery.SourceFormat.PARQUET,
    "json": bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
}


def extract_file_extension(file_name: str) -> str:
    """Extract the file extension from the file path"""
    return file_name.split(".")[-1]


def batch_load_bq(data, context):  # pylint: disable=unused-argument
    """Batch load from GCS to Bigquery"""

    file_extension = extract_file_extension(data["name"])

    # TODO: remove hard coded properties reference
    # TODO: add method for infering the correct config path based on file name
    loader = BigQueryLoader(
        project=PROJECT,
        data_bucket=BUCKET,
        validation_bucket=VALIDATION_BUCKET,
        bq_dataset="test_dataset",
        bq_table="properties",
        file_name=data["name"],
        config_path="config/properties/bq_load.json",
        gcs_client=storage.Client(),
        bq_client=bigquery.Client(),
        source_format=extension_mapping.get(file_extension),
    )

    loader.load_config()
    loader.load()

    logging.info("Job finished")

    # destination_table = client.get_table(dataset_ref.table(TABLE))
    # logging.info("Loaded {} rows.".format(destination_table.num_rows))
