echo "Deploy to project $GCP_PROJECT"
echo "Deploy to region $GCP_FUNCTION_REGION"
echo "Triggered by $GCP_TOPIC_STOCK_CRAWLING topic"
echo "BQ daataset name $BQ_DATASET"
echo "BQ price table name $BQ_PRICE_TABLE_NAME"
echo "BQ stock table name $BQ_STOCK_TABLE_NAME"

gcloud functions deploy set-crawler \
    --entry-point main \
    --source . \
    --project $GCP_PROJECT \
    --runtime python39\
    --region $GCP_FUNCTION_REGION \
    --trigger-topic $GCP_TOPIC_STOCK_CRAWLING  \
    --memory 256MB \
    --max-instances 1 \
    --set-env-vars="GCP_PROJECT"=$GCP_PROJECT \
    --set-env-vars="BQ_DATASET"=$BQ_DATASET \
    --set-env-vars="BQ_PRICE_TABLE_NAME"=$BQ_PRICE_TABLE_NAME \
    --set-env-vars="BQ_STOCK_TABLE_NAME"=$BQ_STOCK_TABLE_NAME \
    --timeout 540s
