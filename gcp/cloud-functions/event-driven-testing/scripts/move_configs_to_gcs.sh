# Sync the validation bucket configs with the configs stored locally in the great expectations
# folder. Ignore anything in the 'uncommitted' folder and the 'plugins' folder
# gsutil -m rm -r gs://$VALIDATION_BUCKET/*
gsutil -m rsync -r -x 'uncommitted/*|.gitignore|plugins/*' great_expectations gs://$VALIDATION_BUCKET
