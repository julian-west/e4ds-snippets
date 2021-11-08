"""Great Expectations Checkpoint"""
import datetime
import logging
import os

from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig
from src.gcs import check_validation_status, read_yml_from_gcs, update_metadata

VALIDATION_BUCKET = os.environ["VALIDATION_BUCKET"]


class ValidationError(Exception):
    """Validation unsuccessful"""

    def __str__(self):
        return "Validation unsuccessful"


def build_data_context(config: DataContextConfig) -> BaseDataContext:
    """Define the great expectations data context"""
    return BaseDataContext(config)


def build_batch_request(
    gcs_file_path: str, batch_spec_passthrough: dict
) -> RuntimeBatchRequest:
    """Build the batch request which specifies which file to test

    Args:
        gcs_file_path (str): gcs file path to the data which needs to be tested
        batch_spec_passthrough (dict): dictionary containing file specific information
            for reading the file. E.g. pd.read_csv arguments

    Returns:
        RuntimeBatchRequest

    """

    return RuntimeBatchRequest(
        datasource_name="my_gcs_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=gcs_file_path,
        runtime_parameters={"path": gcs_file_path},
        batch_identifiers={"default_identifier_name": "default_identifier"},
        batch_spec_passthrough=batch_spec_passthrough,
    )


def run_validation(gcs_file_path: str) -> None:
    """Run the expectation suite"""
    project_config = read_yml_from_gcs(
        VALIDATION_BUCKET, "configs/properties/ge_data_context.yml"
    )
    project_config = DataContextConfig(**project_config)
    batch_spec_passthrough = read_yml_from_gcs(
        VALIDATION_BUCKET, "configs/properties/loading_args.yml"
    )
    context = build_data_context(config=project_config)
    batch_request = build_batch_request(gcs_file_path, batch_spec_passthrough)

    checkpoint_config = {
        "config_version": 1.0,
        "class_name": "Checkpoint",
        "run_name_template": f"%Y%m%d-%H%M%S-{'-'.join(gcs_file_path.split('/')[3:])}",
        "validations": [
            {
                "batch_request": batch_request.to_json_dict(),
                "expectation_suite_name": "properties",
            },
        ],
    }

    checkpoint = SimpleCheckpoint(
        name="properties", data_context=context, **checkpoint_config
    )
    checkpoint_result = checkpoint.run()

    if checkpoint_result["success"]:
        logging.info("Validation successful")
    else:
        logging.error("Validation unsuccessful")
        raise ValidationError


def main(data, context):
    """Cloud function"""
    data_uri = f"gs://{data['bucket']}/{data['name']}"
    if check_validation_status(data["bucket"], data["name"]):
        return "Oject already validated"
    run_validation(data_uri)
    update_metadata(
        data["bucket"],
        data["name"],
        {"validated": True, "validation_ts": datetime.datetime.now()},
    )
