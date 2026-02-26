# Deployment Guide

## Production Deployment on AWS

### Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI configured
3. Docker installed
4. Domain name (optional, for custom domain)

### Step 1: Prepare AWS Account

1. Enable Amazon Bedrock Nova models:
   - Go to AWS Console → Bedrock → Model access
   - Request access to Nova 2 Lite and Nova 2 Omni (preview)
   - Wait for approval (usually instant)

2. Create IAM user with permissions:
   - S3 full access
   - DynamoDB full access
   - Bedrock invoke model access

### Step 2: Initialize Infrastructure

```bash
# Clone repository
git clone <repository-url>
cd creator-dashboard

# Copy and configure environment
cp .env.example .env
# Edit .env with your AWS credentials

# Initialize AWS resources
make init-aws
```

### Step 3: Deploy with Docker

```bash
# Build images
make build

# Start services
make up

# Check logs
make logs
```

### Step 4: Configure Load Balancer (Optional)

For production, use AWS Application Load Balancer:

```bash
# Create ALB
aws elbv2 create-load-balancer \
    --name creator-dashboard-alb \
    --subnets subnet-xxx subnet-yyy \
    --security-groups sg-xxx

# Create target groups for backend and frontend
# Configure health checks
# Update DNS records
```

### Step 5: Set Up CloudFront CDN

```bash
# Create CloudFront distribution for S3 bucket
aws cloudfront create-distribution \
    --origin-domain-name ${S3_BUCKET}.s3.amazonaws.com \
    --default-root-object index.html
```

### Step 6: Configure Auto Scaling

```bash
# For ECS deployment
aws ecs create-service \
    --cluster creator-dashboard \
    --service-name backend \
    --task-definition backend:1 \
    --desired-count 2 \
    --launch-type FARGATE
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (EKS, GKE, or AKS)
- kubectl configured
- Helm installed

### Deploy with Helm

```bash
# Create namespace
kubectl create namespace creator-dashboard

# Create secrets
kubectl create secret generic aws-credentials \
    --from-literal=access-key-id=$AWS_ACCESS_KEY_ID \
    --from-literal=secret-access-key=$AWS_SECRET_ACCESS_KEY \
    -n creator-dashboard

# Deploy with Helm
helm install creator-dashboard ./helm \
    -n creator-dashboard \
    --set aws.region=$AWS_REGION \
    --set aws.s3Bucket=$S3_BUCKET_NAME
```

## Monitoring and Logging

### CloudWatch Integration

```bash
# Create log groups
aws logs create-log-group --log-group-name /creator-dashboard/backend
aws logs create-log-group --log-group-name /creator-dashboard/celery

# Set retention
aws logs put-retention-policy \
    --log-group-name /creator-dashboard/backend \
    --retention-in-days 30
```

### Metrics

Monitor these key metrics:
- API response time
- Video processing time
- Celery queue length
- DynamoDB read/write capacity
- S3 storage usage
- Bedrock API calls

## Backup and Disaster Recovery

### DynamoDB Backups

```bash
# Enable point-in-time recovery
aws dynamodb update-continuous-backups \
    --table-name creator-dashboard-content \
    --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true
```

### S3 Versioning

Already enabled by init script. Configure lifecycle policies:

```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket $S3_BUCKET \
    --lifecycle-configuration file://lifecycle.json
```

## Security Hardening

1. Enable AWS WAF for API protection
2. Use AWS Secrets Manager for sensitive data
3. Enable VPC endpoints for AWS services
4. Implement rate limiting
5. Enable CloudTrail for audit logs

## Cost Optimization

1. Use S3 Intelligent-Tiering
2. Enable DynamoDB auto-scaling
3. Use Spot instances for Celery workers
4. Implement CloudFront caching
5. Set up budget alerts

## Troubleshooting

### Common Issues

1. **Bedrock Access Denied**
   - Verify model access is enabled
   - Check IAM permissions
   - Ensure correct region

2. **Video Processing Timeout**
   - Increase Celery task timeout
   - Scale up worker instances
   - Check FFmpeg installation

3. **High DynamoDB Costs**
   - Review query patterns
   - Add appropriate indexes
   - Consider caching with Redis

## Rollback Procedure

```bash
# Stop current deployment
make down

# Restore previous version
git checkout <previous-tag>
make build
make up

# Restore DynamoDB from backup if needed
aws dynamodb restore-table-from-backup \
    --target-table-name creator-dashboard-content \
    --backup-arn <backup-arn>
```
