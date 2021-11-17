# gsutil rm -r gs://$VALIDATION_BUCKET/configs
# gsutil -m cp -r configs gs://$VALIDATION_BUCKET
gsutil -m rm -r gs://$VALIDATION_BUCKET/*
gsutil -m rsync -r -x 'uncommitted/*|.gitignore|plugins/*' great_expectations gs://$VALIDATION_BUCKET
