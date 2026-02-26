# Architecture Documentation

## System Overview

The Creator Dashboard is a microservices-based platform that automates content creation workflows using AI. The system processes video content, adapts it for multiple platforms, distributes it, and provides analytics and monetization features.

## High-Level Architecture

```
┌─────────────┐
│   Frontend  │ (Next.js)
│   (Port 3000)│
└──────┬──────┘
       │
       │ HTTP/WebSocket
       │
┌──────▼──────┐
│   Backend   │ (FastAPI)
│   (Port 8000)│
└──────┬──────┘
       │
       ├─────────────┬─────────────┬─────────────┐
       │             │             │             │
┌──────▼──────┐ ┌───▼────┐ ┌─────▼─────┐ ┌─────▼─────┐
│   Amazon    │ │ Amazon │ │  Amazon   │ │   Redis   │
│   Bedrock   │ │   S3   │ │ DynamoDB  │ │           │
│ (Nova Models)│ │        │ │           │ │           │
└─────────────┘ └────────┘ └───────────┘ └─────┬─────┘
                                                 │
                                          ┌──────▼──────┐
                                          │   Celery    │
                                          │   Workers   │
                                          └─────────────┘
```

## Components

### 1. Frontend (Next.js)

**Technology**: Next.js 14, React 18, TypeScript, Tailwind CSS

**Responsibilities**:
- User interface and experience
- File upload handling
- Real-time status updates
- Analytics visualization
- Platform management

**Key Features**:
- Server-side rendering for SEO
- React Query for data fetching
- Responsive design
- Real-time WebSocket updates

### 2. Backend API (FastAPI)

**Technology**: Python 3.11, FastAPI, Pydantic

**Responsibilities**:
- RESTful API endpoints
- Authentication and authorization
- Request validation
- Business logic orchestration
- WebSocket connections

**Endpoints**:
- `/auth/*` - Authentication
- `/content/*` - Content management
- `/distribute/*` - Distribution
- `/analytics/*` - Analytics
- `/monetization/*` - Monetization

### 3. Video Processing Service

**Technology**: FFmpeg, OpenCV, Celery

**Responsibilities**:
- Video format validation
- Metadata extraction
- Aspect ratio conversion
- Thumbnail generation
- Quality optimization

**Processing Pipeline**:
1. Upload validation
2. Metadata extraction
3. Platform-specific adaptation
4. Thumbnail generation
5. Quality optimization
6. S3 upload

### 4. AI Services (Amazon Bedrock)

**Models Used**:
- **Nova 2 Lite**: Text generation (titles, descriptions, hashtags)
- **Nova 2 Omni (Preview)**: Vision tasks (ad placement detection, image analysis)

**Use Cases**:
- Platform-specific metadata generation
- Content optimization suggestions
- Trend analysis
- Ad placement detection
- Surface identification

### 5. Storage Layer

#### Amazon S3
- Original video files
- Adapted video files
- Thumbnails
- Temporary processing files

**Structure**:
```
bucket/
├── uploads/{user_id}/{content_id}/
├── adaptations/{content_id}/{platform}/
└── thumbnails/{content_id}/{platform}/
```

#### Amazon DynamoDB
- User data
- Content metadata
- Adaptations
- Publish jobs
- Analytics
- Ad placements

**Tables**:
- `creator-dashboard-users`
- `creator-dashboard-content`
- `creator-dashboard-adaptations`
- `creator-dashboard-publish-jobs`
- `creator-dashboard-analytics`
- `creator-dashboard-ad-placements`

### 6. Caching Layer (Redis)

**Responsibilities**:
- Session management
- API response caching
- Celery message broker
- Rate limiting
- Real-time data

### 7. Background Workers (Celery)

**Tasks**:
- Video processing
- Platform adaptation
- Ad placement analysis
- Analytics collection
- Scheduled publishing

**Configuration**:
- 4 concurrent workers
- 1-hour task timeout
- Automatic retry on failure
- Task result storage in Redis

## Data Flow

### Content Upload Flow

```
1. User uploads video → Frontend
2. Frontend → Backend API (POST /content/upload)
3. Backend generates presigned S3 URL
4. Frontend uploads directly to S3
5. Backend triggers Celery task (process_video_upload)
6. Celery worker:
   - Downloads video from S3
   - Extracts metadata
   - Updates DynamoDB
   - Triggers adaptation task
7. Adaptation task:
   - Generates platform-specific versions
   - Uploads to S3
   - Calls Bedrock for metadata
   - Updates DynamoDB
8. Frontend polls for status updates
```

### Distribution Flow

```
1. User selects platforms → Frontend
2. Frontend → Backend API (POST /distribute)
3. Backend creates publish job in DynamoDB
4. For each platform:
   - Retrieve adaptation from S3
   - Call platform API
   - Update job status
5. Return results to frontend
```

### Analytics Flow

```
1. Celery Beat triggers periodic collection
2. For each published content:
   - Call platform APIs
   - Collect metrics
   - Store in DynamoDB
3. Frontend queries analytics endpoint
4. Backend aggregates and returns data
```

## Security

### Authentication
- JWT tokens with 30-minute expiration
- Bcrypt password hashing
- HTTP-only cookies (optional)

### Authorization
- User-based access control
- Content ownership verification
- Platform token encryption

### Data Protection
- S3 encryption at rest
- HTTPS/TLS in transit
- Presigned URLs for secure access
- IAM roles for AWS services

## Scalability

### Horizontal Scaling
- Stateless backend API (scale with load balancer)
- Multiple Celery workers
- DynamoDB auto-scaling
- S3 unlimited storage

### Vertical Scaling
- Increase worker concurrency
- Larger instance types
- More Redis memory

### Performance Optimization
- Redis caching
- CDN for video delivery
- Database query optimization
- Async processing

## Monitoring

### Metrics
- API response time
- Video processing time
- Queue length
- Error rates
- Resource utilization

### Logging
- Structured JSON logs
- CloudWatch integration
- Error tracking
- Audit trails

### Alerts
- High error rates
- Processing failures
- Resource exhaustion
- Security incidents

## Disaster Recovery

### Backups
- DynamoDB point-in-time recovery
- S3 versioning
- Database snapshots
- Configuration backups

### Recovery Procedures
- Automated failover
- Data restoration
- Service recovery
- Rollback procedures

## Cost Optimization

### Strategies
- S3 Intelligent-Tiering
- DynamoDB on-demand pricing
- Spot instances for workers
- CloudFront caching
- Lifecycle policies

### Monitoring
- AWS Cost Explorer
- Budget alerts
- Resource tagging
- Usage reports
