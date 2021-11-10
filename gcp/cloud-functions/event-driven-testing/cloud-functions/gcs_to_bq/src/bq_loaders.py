"""Support for different file types for loading into Bigquery"""
import json
from dataclasses import dataclass

from google.cloud import bigquery, storage


@dataclass
class BigQueryLoader:
    """Loading data from GCS to Bigquery"""

    project: str
    data_bucket: str
    validation_bucket: str
    bq_dataset: str
    bq_table: str
    file_name: str
    config_path: str
    gcs_client: storage.Client
    bq_client: bigquery.Client
    source_format: bigquery.SourceFormat
    data_uri: str
    table_id: str

    def load_config(self):
        """Load configuration from GCS"""
        bucket = self.gcs_client.get_bucket(self.validation_bucket)
        content = bucket.get_blob(self.config_path).download_as_string()
        self.config = json.loads(content)

    def load(self):
        """Load data into BigQuery"""
        load_job = self.bq_client.load_table_from_uri(
            self.data_uri,
            self.table_id,
            source_format=self.source_format,
            job_config=self.job_config,
        )
        return load_job.result()
