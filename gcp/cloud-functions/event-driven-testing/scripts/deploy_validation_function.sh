gcloud functions deploy data_validation \
    --source data_validation \
    --entry-point main \
    --project $PROJECT \
    --region europe-west2 \
    --env-vars-file data_validation/env.yaml \
    --runtime python39 \
    --memory 512MB \
    --trigger-resource $BUCKET \
    --trigger-event google.storage.object.finalize
