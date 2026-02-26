#!/bin/bash

# Initialize AWS resources for Creator Dashboard
# This script creates S3 bucket and DynamoDB tables

set -e

echo "Initializing AWS resources for Creator Dashboard..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

AWS_REGION=${AWS_REGION:-us-east-1}
S3_BUCKET=${S3_BUCKET_NAME:-creator-dashboard-videos}
TABLE_PREFIX=${DYNAMODB_TABLE_PREFIX:-creator-dashboard}

echo "Region: $AWS_REGION"
echo "S3 Bucket: $S3_BUCKET"
echo "Table Prefix: $TABLE_PREFIX"

# Create S3 bucket
echo "Creating S3 bucket..."
if [ "$AWS_REGION" == "us-east-1" ]; then
    aws s3api create-bucket --bucket $S3_BUCKET --region $AWS_REGION || echo "Bucket may already exist"
else
    aws s3api create-bucket --bucket $S3_BUCKET --region $AWS_REGION \
        --create-bucket-configuration LocationConstraint=$AWS_REGION || echo "Bucket may already exist"
fi

# Enable versioning
aws s3api put-bucket-versioning --bucket $S3_BUCKET \
    --versioning-configuration Status=Enabled

# Set CORS configuration
cat > /tmp/cors.json << EOF
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
EOF

aws s3api put-bucket-cors --bucket $S3_BUCKET --cors-configuration file:///tmp/cors.json

echo "S3 bucket configured successfully"

# Create DynamoDB tables
echo "Creating DynamoDB tables..."

# Users table
aws dynamodb create-table \
    --table-name ${TABLE_PREFIX}-users \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=email,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=email-index,KeySchema=[{AttributeName=email,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION || echo "Table may already exist"

# Content table
aws dynamodb create-table \
    --table-name ${TABLE_PREFIX}-content \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=user_id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=user-index,KeySchema=[{AttributeName=user_id,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION || echo "Table may already exist"

# Adaptations table
aws dynamodb create-table \
    --table-name ${TABLE_PREFIX}-adaptations \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=content_id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=content-index,KeySchema=[{AttributeName=content_id,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION || echo "Table may already exist"

# Publish jobs table
aws dynamodb create-table \
    --table-name ${TABLE_PREFIX}-publish-jobs \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=content_id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=content-index,KeySchema=[{AttributeName=content_id,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION || echo "Table may already exist"

# Analytics table
aws dynamodb create-table \
    --table-name ${TABLE_PREFIX}-analytics \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=content_id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=content-index,KeySchema=[{AttributeName=content_id,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION || echo "Table may already exist"

# Ad placements table
aws dynamodb create-table \
    --table-name ${TABLE_PREFIX}-ad-placements \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=content_id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=content-index,KeySchema=[{AttributeName=content_id,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION || echo "Table may already exist"

echo "DynamoDB tables created successfully"
echo "AWS resources initialization complete!"
