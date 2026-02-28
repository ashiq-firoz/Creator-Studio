# Quick Start Guide

Get the Creator Dashboard running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- AWS account (for production) or use LocalStack (for development)

## Option 1: Local Development (with LocalStack)

Perfect for testing without AWS costs.

### Step 1: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/ashiq-firoz/Creator-Studio.git
cd creator-dashboard

# Copy environment file
cp .env.example .env

# Edit .env and set:
USE_LOCALSTACK=true
LOCALSTACK_ENDPOINT=http://localstack:4566
```

### Step 2: Start Services

- To install make in windows (use cmd in admin mode (run as admin))
```
choco install make
```


```bash
# Build and start all services
make build
make up

# Wait for services to start (about 30 seconds)
```

### Step 3: Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Step 4: Create an Account

1. Go to http://localhost:3000
2. Click "Get Started"
3. Register with email and password
4. Login to access dashboard

### Step 5: Upload Your First Video

1. Navigate to Dashboard
2. Click "Upload" tab
3. Drag and drop a video file (MP4, MOV, or AVI)
4. Add title and description
5. Click upload and watch the magic happen!

## Option 2: Production Setup (with AWS)

For production deployment with real AWS services.

### Step 1: Configure AWS

```bash
# Clone repository
git clone https://github.com/ashiq-firoz/Creator-Studio.git
cd creator-dashboard

# Copy and edit environment
cp .env.example .env

# Edit .env with your AWS credentials:
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
S3_BUCKET_NAME=your-unique-bucket-name
USE_LOCALSTACK=false
```

### Step 2: Enable Bedrock Models

1. Go to AWS Console → Amazon Bedrock
2. Click "Model access" in left sidebar
3. Click "Manage model access"
4. Enable:
   - Amazon Nova Lite
   - Amazon Nova Pro (preview)
5. Click "Save changes"

### Step 3: Initialize AWS Resources

```bash
# Create S3 bucket and DynamoDB tables
make init-aws

# This creates:
# - S3 bucket with versioning and CORS
# - 6 DynamoDB tables with indexes
```

### Step 4: Deploy

```bash
# Build and start services
make build
make up

# Check logs
make logs
```

### Step 5: Verify Deployment

```bash
# Check health
curl http://localhost:8000/health

# Should return: {"status":"healthy","timestamp":"..."}
```

## Common Commands

```bash
# View logs
make logs

# Stop services
make down

# Restart services
make down && make up

# Clean everything
make clean

# Run tests
make test
```

## Troubleshooting

### Services won't start

```bash
# Check Docker is running
docker ps

# Check logs for errors
make logs

# Rebuild images
make clean
make build
make up
```

### Can't connect to backend

```bash
# Check backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Verify port 8000 is not in use
netstat -an | grep 8000  # Linux/Mac
netstat -an | findstr 8000  # Windows
```

### Video upload fails

```bash
# Check Celery worker is running
docker-compose ps celery-worker

# Check worker logs
docker-compose logs celery-worker

# Verify FFmpeg is installed in container
docker-compose exec backend ffmpeg -version
```

### Bedrock API errors

1. Verify model access is enabled in AWS Console
2. Check AWS credentials in .env
3. Ensure you're in a supported region (us-east-1, us-west-2)
4. Check IAM permissions include bedrock:InvokeModel

### DynamoDB errors

```bash
# List tables
aws dynamodb list-tables

# Check table exists
aws dynamodb describe-table --table-name creator-dashboard-users

# Recreate tables if needed
make init-aws
```

## Next Steps

### Add Social Media Integration

Edit `.env` and add your API credentials:

```bash
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
INSTAGRAM_APP_ID=your_instagram_app_id
INSTAGRAM_APP_SECRET=your_instagram_app_secret
TIKTOK_CLIENT_KEY=your_tiktok_client_key
TIKTOK_CLIENT_SECRET=your_tiktok_client_secret
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
```

**Don't have these credentials yet?** Follow the step-by-step guide: [SOCIAL_MEDIA_API_SETUP.md](SOCIAL_MEDIA_API_SETUP.md)

Restart services:
```bash
make down && make up
```

### Configure Custom Domain

1. Set up AWS Application Load Balancer
2. Configure SSL certificate
3. Update DNS records
4. Update CORS settings in backend

### Enable Monitoring

1. Set up CloudWatch logs
2. Configure alerts
3. Enable X-Ray tracing
4. Set up cost alerts

### Scale for Production

```bash
# Scale Celery workers
docker-compose up -d --scale celery-worker=4

# Enable DynamoDB auto-scaling
aws application-autoscaling register-scalable-target \
    --service-namespace dynamodb \
    --resource-id table/creator-dashboard-content \
    --scalable-dimension dynamodb:table:ReadCapacityUnits \
    --min-capacity 5 \
    --max-capacity 100
```

## Testing the Platform

### Test Video Upload

```bash
# Upload a test video via API
curl -X POST http://localhost:8000/content/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test-video.mp4" \
  -F "title=Test Video" \
  -F "description=Testing upload"
```

### Test Platform Adaptation

```bash
# Get adaptations for content
curl http://localhost:8000/content/{content_id}/adaptations \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Distribution

```bash
# Distribute to platforms
curl -X POST http://localhost:8000/distribute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "your-content-id",
    "platforms": ["youtube", "instagram", "tiktok"],
    "immediate": true
  }'
```

## Getting Help

- Check README.md for detailed documentation
- Review ARCHITECTURE.md for system design
- See DEPLOYMENT.md for production setup
- Check logs: `make logs`
- Open an issue on GitHub

## What's Next?

1. Upload your first video
2. Review generated adaptations
3. Test distribution to platforms
4. Check analytics dashboard
5. Explore monetization features

Happy creating! 🎬
