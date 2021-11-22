# Create GCS buckets
# One for the data and one for hosting data validation configurations
REGION=europe-west2

gsutil mb -c standard -p $PROJECT -l $REGION gs://${PROJECT}-${REGION}-data
gsutil mb -c standard -p $PROJECT -l $REGION gs://${PROJECT}-${REGION}-validation-configs
