"""Support for different file types for loading into Bigquery"""
import json
from dataclasses import dataclass
from typing import Optional

from google.cloud import bigquery, storage


@dataclass
class ProjectConfig:
    """Class for storing project configuration variables"""

    project: str
    data_bucket: str
    validation_bucket: str
    bq_dataset: str
    bq_table: str


class BigQueryLoader:
    """Loading data from GCS to Bigquery"""

    def __init__(
        self,
        project_config: ProjectConfig,
        file_name: str,
        source_format: str,
        config_path: Optional[str] = None,
        gcs_client: storage.Client = storage.Client(),
        bq_client=storage.Client(),
    ):
        self.project_config = project_config
        self.file_name = file_name
        self.config_path = config_path
        self.gcs_client = gcs_client
        self.bq_client = bq_client
        self.source_format = source_format

        self.data_uri = self._build_uri()
        self.table_id = self._build_table_id()
        self.job_params = self._load_job_config()
        self.job_config = self._build_job_config()

    def _build_uri(self) -> str:
        """Build full GCS URI to data object"""
        return f"gs://{self.project_config.data_bucket}/{self.file_name}"

    def _build_table_id(self) -> str:
        """Build the full Biquery table ID"""
        return (
            f"{self.project_config.project}"
            f".{self.project_config.bq_dataset}"
            f".{self.project_config.bq_table}"
        )

    def _load_job_config(self) -> dict:
        """Load configuration from GCS"""
        if self.config_path:
            bucket = self.gcs_client.get_bucket(self.project_config.validation_bucket)
            content = bucket.get_blob(self.config_path).download_as_string()
            return json.loads(content)
        else:
            return {}

    def _build_job_config(self) -> bigquery.LoadJobConfig:
        """Create LoadJobConfig object"""

        return bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            source_format=self.source_format,
            **self.job_params,
        )

    def load(self):
        """Load data into BigQuery"""
        load_job = self.bq_client.load_table_from_uri(
            self.data_uri,
            self.table_id,
            job_config=self.job_config,
        )
        return load_job.result()
