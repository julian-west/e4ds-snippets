gcloud functions deploy test \
    --source cloud-functions/test \
    --entry-point hello_gcs \
    --project $PROJECT \
    --region europe-west2 \
    --runtime python39 \
    --trigger-resource $BUCKET \
    --trigger-event google.storage.object.metadataUpdate
