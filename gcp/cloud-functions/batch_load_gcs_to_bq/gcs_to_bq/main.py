"""Move data from GCS to BigQuery"""
import logging
import os

from google.cloud import bigquery, storage
from src.bq_loaders import BigQueryLoader, ProjectConfig
from src.utils import extract_table_name, identify_source_format

PROJECT = os.environ["PROJECT"]
BUCKET = os.environ["BUCKET"]
VALIDATION_BUCKET = os.environ["VALIDATION_BUCKET"]
BQ_DATASET = os.environ["BQ_DATASET"]
EXTENSION_MAPPING = {
    "csv": bigquery.SourceFormat.CSV,
    "avro": bigquery.SourceFormat.AVRO,
    "parquet": bigquery.SourceFormat.PARQUET,
    "json": bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
}


def batch_load_bq(data, context):  # pylint: disable=unused-argument
    """Batch load from GCS to Bigquery"""

    table_name = extract_table_name(data["name"])
    source_format = identify_source_format(
        data["name"], supported_file_extensions=EXTENSION_MAPPING
    )
    project_config = ProjectConfig(
        project=PROJECT,
        data_bucket=BUCKET,
        validation_bucket=VALIDATION_BUCKET,
        bq_dataset=BQ_DATASET,
        bq_table=table_name,
    )

    loader = BigQueryLoader(
        project_config=project_config,
        file_name=data["name"],
        config_path=f"configs/{table_name}/bq_load.json",
        gcs_client=storage.Client(),
        bq_client=bigquery.Client(),
        source_format=source_format,
    )

    logging.info(f"Loading {loader.data_uri} into {loader.table_id}")
    result = loader.load()
    print(result)
    logging.info("Job finished")


# TODO: update metadata/rename file after uploading
