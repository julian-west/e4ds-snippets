"""Loading functions from GCS"""
import logging
import os

import ruamel.yaml as yaml
from google.cloud import storage


def read_yml_from_gcs(
    gcs_bucket: str, file_name: str, client: storage.Client = storage.Client()
) -> dict:
    """Read YAML file from GCS location"""
    bucket: storage.bucket.Bucket = client.get_bucket(gcs_bucket)
    content: str = bucket.blob(file_name).download_as_string()
    # TODO: Move to general function
    content = (
        content.decode("utf-8")
        .replace("${PROJECT}", os.environ["PROJECT"])
        .replace("${VALIDATION_BUCKET}", os.environ["VALIDATION_BUCKET"])
    )
    return yaml.safe_load(content)


def update_metadata(
    gcs_bucket: str,
    file_name: str,
    metadata: dict,
    client: storage.Client = storage.Client(),
) -> None:
    """Set a blob's metadata."""
    bucket = client.bucket(gcs_bucket)
    blob = bucket.get_blob(file_name)
    blob.metadata = metadata
    blob.patch()

    logging.info("The metadata for the blob {} is {}".format(blob.name, blob.metadata))


def check_validation_status(
    gcs_bucket: str,
    file_name: str,
    client: storage.Client = storage.Client(),
) -> bool:
    """Check if object has already been validated"""
    bucket = client.bucket(gcs_bucket)
    blob = bucket.get_blob(file_name)
    if isinstance(blob.metadata, dict):
        if blob.metadata.get("validated"):
            return True
        else:
            return False
    else:
        return False
