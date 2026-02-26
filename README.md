# Creator Dashboard

AI-powered platform for content adaptation, distribution, and monetization using Amazon Bedrock Nova models.

## Features

- **One-Click Cross-Platform Adaptation**: Upload once, automatically adapt for YouTube, Instagram, TikTok, and Twitter
- **AI-Powered Content Generation**: Uses Amazon Bedrock Nova 2 Lite for text generation and Nova 2 Omni for vision tasks
- **Unified Distribution**: Schedule or publish instantly across all platforms
- **Intelligent Analytics**: Real-time performance tracking and trend predictions
- **Smart Monetization**: AI-powered ad placement detection and revenue optimization

## Architecture

### Backend
- FastAPI (Python 3.11)
- Amazon S3 for video storage
- Amazon DynamoDB for data persistence
- Amazon Bedrock (Nova 2 Lite & Nova 2 Omni)
- Redis for caching
- Celery for background tasks
- FFmpeg for video processing

### Frontend
- Next.js 14 with TypeScript
- React Query for data fetching
- Tailwind CSS for styling
- React Dropzone for file uploads

## Prerequisites

- Docker and Docker Compose
- AWS Account with:
  - S3 access
  - DynamoDB access
  - Bedrock access (Nova models enabled)
- AWS CLI configured (for production setup)

## Quick Start (Development with LocalStack)

1. Clone the repository:
```bash
git clone <repository-url>
cd creator-dashboard
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Start services with Docker Compose:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Production Setup

### 1. Configure AWS Credentials

Edit `.env` file with your AWS credentials:
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=your-bucket-name
DYNAMODB_TABLE_PREFIX=creator-dashboard

# Disable LocalStack for production
USE_LOCALSTACK=false
```

### 2. Initialize AWS Resources

Run the initialization script:
```bash
chmod +x scripts/init-aws.sh
./scripts/init-aws.sh
```

This creates:
- S3 bucket with versioning and CORS
- DynamoDB tables with GSIs
- Proper IAM permissions

### 3. Configure Social Media APIs

Add your social media API credentials to `.env`:
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

### 4. Deploy with Docker

```bash
docker-compose -f docker-compose.yml up -d
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token
- `GET /auth/me` - Get current user info

### Content Management
- `POST /content/upload` - Upload video content
- `GET /content` - List user's content
- `GET /content/{content_id}` - Get content details
- `GET /content/{content_id}/adaptations` - Get platform adaptations

### Distribution
- `POST /distribute` - Distribute content to platforms
- `GET /distribute/{job_id}` - Get distribution status

### Analytics
- `GET /analytics/{content_id}` - Get content analytics
- `POST /analytics/trends` - Get trend predictions

### Monetization
- `POST /monetization/analyze/{content_id}` - Analyze ad opportunities
- `GET /monetization/{content_id}/placements` - Get ad placements

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running Celery Worker

```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

### Running Celery Beat

```bash
cd backend
celery -A app.celery_app beat --loglevel=info
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### View Logs
```bash
# Backend logs
docker-compose logs -f backend

# Celery worker logs
docker-compose logs -f celery-worker

# Frontend logs
docker-compose logs -f frontend
```

## Scaling

### Horizontal Scaling

Scale Celery workers:
```bash
docker-compose up -d --scale celery-worker=4
```

### Database Optimization

DynamoDB tables use PAY_PER_REQUEST billing mode for automatic scaling.

For predictable workloads, switch to PROVISIONED mode:
```bash
aws dynamodb update-table \
    --table-name creator-dashboard-content \
    --billing-mode PROVISIONED \
    --provisioned-throughput ReadCapacityUnits=100,WriteCapacityUnits=100
```

## Security

- All API endpoints require JWT authentication
- S3 uses presigned URLs for secure uploads
- DynamoDB uses IAM roles for access control
- Secrets managed via environment variables
- HTTPS required in production

## Cost Optimization

- Use S3 Intelligent-Tiering for video storage
- Enable DynamoDB auto-scaling
- Use Bedrock on-demand pricing
- Implement CloudFront CDN for video delivery
- Set up S3 lifecycle policies for old content

## Troubleshooting

### Video Processing Fails
- Check FFmpeg installation: `docker-compose exec backend ffmpeg -version`
- Verify video format is supported (MP4, MOV, AVI)
- Check Celery worker logs

### Bedrock API Errors
- Verify Bedrock access in your AWS region
- Ensure Nova models are enabled in your account
- Check AWS credentials and permissions

### Database Connection Issues
- Verify DynamoDB tables exist: `aws dynamodb list-tables`
- Check AWS credentials in `.env`
- For LocalStack: ensure service is running


