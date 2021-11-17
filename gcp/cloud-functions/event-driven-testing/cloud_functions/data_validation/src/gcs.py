"""Loading functions from GCS"""
import logging
from typing import Any

import ruamel.yaml as yaml
from google.cloud import storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def read_yml_from_gcs(
    bucket_name: str,
    blob_name: str,
    template: dict[str, Any],
    client: storage.Client = storage.Client(),
) -> dict[str, Any]:
    """Read YAML file from GCS location and replace template with variables

    Args:
        bucket_name (str): name of GCS bucket
        blob_name (str): GCS file path
        template (dict): dictionary containing pairs of template strings present in
            yaml file and the string to replace it with
        client (storage.Client): GCS storage client

    Returns:
        dictionary of the read yaml file with the template strings replaced
    """

    bucket: storage.Bucket = client.get_bucket(bucket_name)
    content: bytes = bucket.blob(blob_name).download_as_string()
    decoded: str = content.decode("utf-8")

    for k, v in template.items():
        decoded = decoded.replace(k, v)

    return yaml.safe_load(decoded)


def move_blob(
    bucket_name: str,
    blob_name: str,
    prefix: str,
    client: storage.Client = storage.Client(),
) -> None:
    """Moves (renames) a blob in GCS

    Args:
        bucket_name (str): name of GCS bucket
        blob_name (str): GCS file path
        prefix (str): GCS 'folder' to move the file
        client (storage.Client): GCS storage client

    """

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    new_name = "/".join([prefix] + blob_name.split("/")[1:])
    new_blob = bucket.rename_blob(blob, new_name)

    logger.info(f"Blob {blob.name} has been renamed to {new_blob.name}")


def check_trigger_file_path(blob_name: str, trigger_prefix: str) -> bool:
    """Check the file path before triggering a cloud function

    Args:
        blob_name (str): GCS file path
        trigger_prefix (str): GCS 'folder' that should trigger the rest of the function

    Returns:
        bool: True if the blob_name starts with the specified trigger prefix

    """
    return blob_name.startswith(trigger_prefix)


def extract_dataset_name(blob_name) -> str:
    """Get dataset name from the GCS second level 'folder'

    Example:
        extract_dataset_name("landing_zone/properties/properties.csv")
        >>>'properties'

    """
    return blob_name.split("/")[1]
