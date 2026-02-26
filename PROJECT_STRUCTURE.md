# Project Structure

```
creator-dashboard/
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI application entry point
│   │   ├── config.py                # Configuration and settings
│   │   ├── models.py                # Pydantic models
│   │   ├── database.py              # DynamoDB client and operations
│   │   ├── auth.py                  # Authentication and JWT handling
│   │   ├── aws_services.py          # S3 and Bedrock integrations
│   │   ├── video_processor.py       # Video processing utilities
│   │   ├── celery_app.py            # Celery configuration
│   │   └── tasks.py                 # Celery background tasks
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py           # Model tests
│   │   └── test_video_processor.py  # Video processing tests
│   ├── Dockerfile                   # Backend container definition
│   ├── requirements.txt             # Python dependencies
│   └── pytest.ini                   # Pytest configuration
│
├── frontend/                         # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx               # Root layout
│   │   ├── page.tsx                 # Landing page
│   │   ├── globals.css              # Global styles
│   │   ├── providers.tsx            # React Query provider
│   │   └── dashboard/
│   │       └── page.tsx             # Dashboard page
│   ├── components/
│   │   ├── UploadSection.tsx        # Video upload component
│   │   └── ContentList.tsx          # Content list component
│   ├── lib/
│   │   └── api.ts                   # API client
│   ├── Dockerfile                   # Frontend container definition
│   ├── package.json                 # Node dependencies
│   ├── tsconfig.json                # TypeScript configuration
│   ├── tailwind.config.js           # Tailwind CSS configuration
│   ├── postcss.config.js            # PostCSS configuration
│   └── next.config.js               # Next.js configuration
│
├── scripts/
│   └── init-aws.sh                  # AWS infrastructure initialization
│
├── .kiro/
│   └── specs/
│       └── creator-dashboard/
│           ├── requirements.md      # Requirements specification
│           ├── desgn.md            # Design document
│           └── tasks.md            # Implementation tasks
│
├── docker-compose.yml               # Docker Compose configuration
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── Makefile                         # Build and deployment commands
├── README.md                        # Project documentation
├── ARCHITECTURE.md                  # Architecture documentation
├── DEPLOYMENT.md                    # Deployment guide
└── PROJECT_STRUCTURE.md            # This file
```

## Key Files Description

### Backend

- **main.py**: FastAPI application with all API endpoints (auth, content, distribution, analytics, monetization)
- **config.py**: Environment-based configuration using Pydantic Settings
- **models.py**: Data models for requests/responses and business entities
- **database.py**: DynamoDB client with CRUD operations for all tables
- **auth.py**: JWT authentication, password hashing, user verification
- **aws_services.py**: S3 file operations and Bedrock AI model integrations
- **video_processor.py**: FFmpeg-based video processing, format conversion, thumbnail generation
- **celery_app.py**: Celery configuration for background task processing
- **tasks.py**: Async tasks for video processing, adaptation, analytics collection

### Frontend

- **app/page.tsx**: Landing page with feature showcase
- **app/dashboard/page.tsx**: Main dashboard with tabs for upload, content, analytics, monetization
- **components/UploadSection.tsx**: Drag-and-drop video upload with progress tracking
- **components/ContentList.tsx**: Display user's content with status and actions
- **lib/api.ts**: Axios-based API client with authentication interceptor

### Infrastructure

- **docker-compose.yml**: Multi-container setup with backend, frontend, Redis, Celery workers, LocalStack
- **scripts/init-aws.sh**: Bash script to create S3 bucket and DynamoDB tables
- **Makefile**: Convenient commands for build, deploy, test, and cleanup

## Technology Stack

### Backend
- Python 3.11
- FastAPI (async web framework)
- Boto3 (AWS SDK)
- Celery (task queue)
- FFmpeg (video processing)
- OpenCV (computer vision)
- Redis (caching and message broker)

### Frontend
- Next.js 14 (React framework)
- TypeScript
- Tailwind CSS
- React Query (data fetching)
- Axios (HTTP client)
- React Dropzone (file uploads)

### AWS Services
- Amazon Bedrock (Nova 2 Lite, Nova 2 Omni)
- Amazon S3 (video storage)
- Amazon DynamoDB (database)

### DevOps
- Docker & Docker Compose
- LocalStack (local AWS emulation)
- Pytest (testing)
- GitHub Actions (CI/CD ready)

## Environment Variables

Required environment variables (see .env.example):

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET_NAME=creator-dashboard-videos
DYNAMODB_TABLE_PREFIX=creator-dashboard

# Bedrock Models
BEDROCK_MODEL_TEXT=us.amazon.nova-lite-v1:0
BEDROCK_MODEL_VISION=us.amazon.nova-pro-v1:0

# Security
JWT_SECRET=your_secret_key

# Redis
REDIS_URL=redis://redis:6379

# Social Media APIs (optional)
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
INSTAGRAM_APP_ID=
INSTAGRAM_APP_SECRET=
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TWITTER_API_KEY=
TWITTER_API_SECRET=
```

## Development Workflow

1. **Setup**: Copy `.env.example` to `.env` and configure
2. **Build**: `make build` to build Docker images
3. **Start**: `make up` to start all services
4. **Develop**: Edit code (hot reload enabled)
5. **Test**: `make test` to run tests
6. **Logs**: `make logs` to view service logs
7. **Stop**: `make down` to stop services

## Production Deployment

1. Configure AWS credentials in `.env`
2. Run `make init-aws` to create infrastructure
3. Update social media API credentials
4. Deploy with `make up`
5. Configure load balancer and domain
6. Set up monitoring and alerts

## API Endpoints

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - Login
- GET `/auth/me` - Get current user

### Content
- POST `/content/upload` - Upload video
- GET `/content` - List content
- GET `/content/{id}` - Get content details
- GET `/content/{id}/adaptations` - Get adaptations

### Distribution
- POST `/distribute` - Distribute to platforms
- GET `/distribute/{job_id}` - Get status

### Analytics
- GET `/analytics/{content_id}` - Get analytics
- POST `/analytics/trends` - Get trend predictions

### Monetization
- POST `/monetization/analyze/{content_id}` - Analyze ad opportunities
- GET `/monetization/{content_id}/placements` - Get placements

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
make test
```

## Monitoring

- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`
- Logs: `make logs`

## Support

For issues and questions, refer to:
- README.md - Getting started guide
- ARCHITECTURE.md - System architecture
- DEPLOYMENT.md - Deployment instructions
