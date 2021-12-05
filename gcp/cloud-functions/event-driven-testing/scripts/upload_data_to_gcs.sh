# Upload data from data dir to GCS
TARGET_FOLDER=${BUCKET}/landing_zone/properties/
echo "Moving data to ${TARGET_FOLDER}"
gsutil cp data/properties/properties.csv gs://$TARGET_FOLDER
gsutil cp data/properties_bad/properties_bad.csv gs://$TARGET_FOLDER
