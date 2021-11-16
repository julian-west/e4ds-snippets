"""Great Expectations Checkpoint"""
import logging
import os
from typing import Any

from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig
from src.gcs import check_trigger_file_path, move_blob, read_yml_from_gcs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

VALIDATION_BUCKET = os.environ["VALIDATION_BUCKET"]
YAML_TEMPLATE = {"$VALIDATION_BUCKET": VALIDATION_BUCKET}


class ValidationError(Exception):
    """Validation Unsuccessful Exception"""


def build_data_context_config(config: dict[str, Any]) -> DataContextConfig:
    """Build the data context config from a dictionary"""
    return DataContextConfig(**config)


def build_data_context(config: DataContextConfig) -> BaseDataContext:
    """Define the great expectations data context"""
    return BaseDataContext(config)


def build_batch_request(
    gcs_file_path: str, batch_spec_passthrough: dict[str, Any]
) -> RuntimeBatchRequest:
    """Build the batch request which specifies which data file to test

    Args:
        gcs_file_path (str): gcs file path to the data which needs to be tested
        batch_spec_passthrough (dict): dictionary containing file specific information
            for reading the file. E.g. the pd.read_csv arguments

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


def build_checkpoint(
    checkpoint_name: str,
    expectation_suite_name: str,
    context: BaseDataContext,
    batch_request: RuntimeBatchRequest,
) -> SimpleCheckpoint:
    """Build the great expectations checkpoint"""
    file_name = "-".join(batch_request.data_asset_name.split("/")[3:])

    checkpoint_config = {
        "config_version": 1.0,
        "class_name": "Checkpoint",
        "run_name_template": f"%Y%m%d-%H%M%S-{file_name}",
        "validations": [
            {
                "batch_request": batch_request.to_json_dict(),
                "expectation_suite_name": expectation_suite_name,
            },
        ],
    }

    return SimpleCheckpoint(
        name=checkpoint_name, data_context=context, **checkpoint_config
    )


def run_validation(gcs_uri: str) -> str:
    """Run the expectation suite"""

    project_config = read_yml_from_gcs(
        bucket_name=VALIDATION_BUCKET,
        blob_name="configs/properties/ge_data_context.yml",
        template=YAML_TEMPLATE,
    )

    batch_spec_passthrough = read_yml_from_gcs(
        bucket_name=VALIDATION_BUCKET,
        blob_name="configs/properties/loading_args.yml",
        template=YAML_TEMPLATE,
    )

    context_config = build_data_context_config(project_config)
    context = build_data_context(config=context_config)
    batch_request = build_batch_request(gcs_uri, batch_spec_passthrough)
    checkpoint = build_checkpoint(
        checkpoint_name="properties",
        expectation_suite_name="properties",
        context=context,
        batch_request=batch_request,
    )

    logger.info(f"Starting Validation for {gcs_uri}")
    checkpoint_result = checkpoint.run()

    if checkpoint_result["success"]:
        logger.info("Validation successful")
    else:
        logger.error("Validation unsuccessful")
        raise ValidationError

    return checkpoint_result["success"]


def main(data, context):  # pylint: disable=unused-argument
    """Cloud function"""
    if not check_trigger_file_path(data["name"], "landing_zone"):
        return

    data_uri = f"gs://{data['bucket']}/{data['name']}"
    success = run_validation(data_uri)
    if success:
        move_blob(
            bucket_name=data["bucket"], blob_name=data["name"], prefix="validated"
        )
    else:
        move_blob(
            bucket_name=data["bucket"],
            blob_name=data["name"],
            prefix="failed_validation",
        )
