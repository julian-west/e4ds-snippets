# Create GCS buckets
# One for the data and one for hosting configurations
REGION=europe-west2
BUCKET_PREFIX=${PROJECT}-${REGION}

gsutil mb -c standard -p $PROJECT -l $REGION gs://${PROJECT}-${REGION}-data
gsutil mb -c standard -p $PROJECT -l $REGION gs://${PROJECT}-${REGION}-validation-configs
