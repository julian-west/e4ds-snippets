gsutil rm -r gs://$VALIDATION_BUCKET/configs
gsutil -m cp -r configs gs://$VALIDATION_BUCKET
