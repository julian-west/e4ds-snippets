import os

from google.cloud import storage


def set_blob_metadata(bucket_name, blob_name, metadata):
    """Set a blob's metadata."""
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    blob.metadata = metadata
    blob.patch()

    print("The metadata for the blob {} is {}".format(blob.name, blob.metadata))


def get_blob_metadata(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    return blob.metadata


if __name__ == "__main__":
    BUCKET = os.environ["BUCKET"]
    FILE = "uk_properties_properties_data_1_test.csv"
    FILE = "uk_properties_properties_data_8.csv"
    METADATA = {"validated": True}

    # set_blob_metadata(BUCKET, FILE, METADATA)
    print(get_blob_metadata(BUCKET, FILE))
