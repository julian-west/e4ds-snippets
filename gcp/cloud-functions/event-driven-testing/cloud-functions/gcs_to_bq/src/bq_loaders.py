"""Support for different file types for loading into Bigquery"""
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from google.cloud import bigquery, storage


class BigQueryLoader(ABC):
    """Loading data from GCS to Bigquery"""

    write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    def __init__(
        self,
        project: str,
        file_name: str,
        data_bucket: str,
        validation_bucket: str,
        bq_dataset: str,
        bq_table: str,
        config_path: str,
    ):
        self.project = project
        self.file_name = file_name
        self.data_bucket = data_bucket
        self.validation_bucket = validation_bucket
        self.bq_dataset = bq_dataset
        self.bq_table = bq_table
        self.config_path = config_path
        self.job_config: Optional[bigquery.LoadJobConfig] = None

        self.data_uri = f"gs://{data_bucket}/{file_name}"
        self.table_id = f"{project}.{bq_dataset}.{bq_table}"
        self.gcs_client = storage.Client(project=self.project)
        self.bq_client = bigquery.Client(project=self.project)

    def load_config(self):
        """Load configuration from GCS"""
        bucket: storage.Bucket = self.gcs_client.get_bucket(self.validation_bucket)
        content: bytes = bucket.get_blob(self.config_path).download_as_string()
        self.config: dict = json.loads(content)

    @abstractmethod
    def build_config(self):
        """Create bigquery job_config object"""

    def load(self):
        """Load data into BigQuery"""
        if self.job_config:
            load_job = self.bq_client.load_table_from_uri(
                self.data_uri, self.table_id, job_config=self.job_config
            )
            return load_job.result()


class CsvBigQueryLoader(BigQueryLoader):
    source_format = bigquery.SourceFormat.CSV

    def build_config(self):
        self.job_config = bigquery.LoadJobConfig(
            write_disposition=self.write_disposition,
            source_format=self.source_format,
            **self.config,
        )


@dataclass
class AvroBigQueryLoader(BigQueryLoader):
    source_format = bigquery.SourceFormat.AVRO

    def build_config(self):
        pass


@dataclass
class ParquetBigQueryLoader(BigQueryLoader):
    source_format = bigquery.SourceFormat.PARQUET

    def build_config(self):
        pass


@dataclass
class NewLineJsonBigQueryLoader(BigQueryLoader):
    source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    def build_config(self):
        pass
