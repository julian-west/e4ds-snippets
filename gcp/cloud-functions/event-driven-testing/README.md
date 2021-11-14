# Event Driven Testing on Google Cloud with Great Expectations

## Directory Structure

```
├── cloud_functions
│   └── data_validation                     <- cloud function directory to validate data
│       ├── main.py
│       └── src
│           └── gcs.py                      <- Google Cloud Storage utility functions
├── configs
│   └── properties
│       ├── expectations
│       │   └── properties.json             <- great expectations data expectations
│       ├── ge_data_context.yml             <- great expectations config
│       └── loading_args.yml                <- great expectations data loading args
├── data
├── data_generator                          <- module to generate fake properties data
│   ├── data_generator.py                   <- data generator script
│   └── properties.py                       <- property definitions and attributes
└── scripts
    ├── create_resources.sh                 <- create GCS buckets
    ├── deploy_validation_function.sh       <- deploy the validation function on GCP
    ├── move_configs_to_gcs.sh              <- move configs from local to GCS location
    └── render_data_docs.sh                 <- render the great expectations data docs locally

```


## Getting Started

Set the following environment variables:
```
PROJECT=<your-GCP-project>
BUCKET=<your-gcs-bucket-name-for-storing-data>
VALIDATION_BUCKET=<your-gcs-bucket-name-for-storing-validation-configs>
```

Create a virtual Python environment using the top level requirements.txt file. For example:
```
# using pyenv
pyenv virtualenv 3.9.5 data_validation_cloud_functions
pyenv activate data_validation_cloud_functions
```

## Data Generation

A fake 'properties' dataset was created for the purposes of testing the data validation cloud function.

The different property types and their specific attributes are defined in the `data_generator/properties.py` file.

To generate a fake dataset can be created by running the `data_generator.py` script from the `data_generator` module. For example:
```
cd data_generator
python data_generator.py
```
Once the fake dataset has been generated you can copy the `csv` file into your Google Cloud Storage bucket to trigger the cloud function (if the cloud function has been deployed)
