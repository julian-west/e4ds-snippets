# Copy the data docs to local computer to render the great expectations validation results UI
# Data docs will be available in the data_docs folder which is not under version control
# The index.html will open automatically
set -e

if [ -z "$1" ]
then
    VALIDATION_BUCKET=$VALIDATION_BUCKET
else
    VALIDATION_BUCKET=$1
fi

if [ -z "$VALIDATION_BUCKET" ]
then
    echo "No bucket specified: Set the \$VALIDATION_BUCKET env variable or supply the bucket name as an argument"
    echo "Aborting..."
    exit 1
fi

rm -rf data_docs
mkdir data_docs
gsutil -m cp -r gs://$VALIDATION_BUCKET/* ./data_docs/
open data_docs/index.html
