from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from .models import (
    UserCreate, UserResponse, Token, ContentUploadResponse,
    PublishRequest, PublishResponse, Platform, UploadStatus,
    PublishStatus, SubscriptionTier, AnalyticsMetrics, TrendPrediction
)
from .auth import get_password_hash, verify_password, create_access_token, get_current_user
from .database import db
from .aws_services import s3_service, bedrock_service
from .tasks import process_video_upload, generate_platform_adaptations, analyze_ad_placements, collect_analytics

app = FastAPI(
    title="Creator Dashboard API",
    description="AI-powered content adaptation, distribution, and monetization platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        db.create_tables()
        print("Database tables initialized")
    except Exception as e:
        print(f"Error initializing database: {e}")


@app.get("/")
async def root():
    return {"message": "Creator Dashboard API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register a new user"""
    # Check if user exists
    existing_user = db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user_data = {
        "email": user.email,
        "username": user.username,
        "password_hash": get_password_hash(user.password),
        "subscription_tier": SubscriptionTier.FREE.value,
        "connected_platforms": []
    }
    
    user_id = db.create_user(user_data)
    created_user = db.get_user(user_id)
    
    return UserResponse(
        id=created_user['id'],
        email=created_user['email'],
        username=created_user['username'],
        subscription_tier=SubscriptionTier(created_user['subscription_tier']),
        connected_platforms=[],
        created_at=datetime.fromisoformat(created_user['created_at'])
    )


@app.post("/auth/login", response_model=Token)
async def login(email: str, password: str):
    """Login and get access token"""
    user = db.get_user_by_email(email)
    
    if not user or not verify_password(password, user['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user['id']})
    return Token(access_token=access_token)


@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user['id'],
        email=current_user['email'],
        username=current_user['username'],
        subscription_tier=SubscriptionTier(current_user['subscription_tier']),
        connected_platforms=[Platform(p) for p in current_user.get('connected_platforms', [])],
        created_at=datetime.fromisoformat(current_user['created_at'])
    )


# Content management endpoints
@app.post("/content/upload", response_model=ContentUploadResponse)
async def upload_content(
    file: UploadFile = File(...),
    title: str = "Untitled",
    description: str = "",
    current_user: dict = Depends(get_current_user)
):
    """Upload video content"""
    # Validate file type
    if not file.content_type.startswith('video/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a video"
        )
    
    # Generate content ID and S3 key
    content_id = str(uuid.uuid4())
    s3_key = f"uploads/{current_user['id']}/{content_id}/{file.filename}"
    
    # Generate presigned URL for upload
    upload_url = s3_service.generate_presigned_upload_url(s3_key, file.content_type)
    
    # Create content record
    content_data = {
        "user_id": current_user['id'],
        "original_file_url": f"s3://{s3_service.bucket_name}/{s3_key}",
        "title": title,
        "description": description,
        "upload_status": UploadStatus.PENDING.value,
        "file_size": 0  # Will be updated after upload
    }
    
    db.create_content(content_data)
    
    # Note: In production, you'd upload the file here or use the presigned URL
    # For now, we'll trigger processing assuming upload is complete
    process_video_upload.delay(content_id, s3_key)
    
    return ContentUploadResponse(
        content_id=content_id,
        upload_url=upload_url,
        status=UploadStatus.PENDING
    )


@app.get("/content/{content_id}")
async def get_content(content_id: str, current_user: dict = Depends(get_current_user)):
    """Get content details"""
    content = db.get_content(content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return content


@app.get("/content/{content_id}/adaptations")
async def get_content_adaptations(content_id: str, current_user: dict = Depends(get_current_user)):
    """Get platform adaptations for content"""
    content = db.get_content(content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    adaptations = db.get_content_adaptations(content_id)
    return {"content_id": content_id, "adaptations": adaptations}


@app.get("/content")
async def list_user_content(current_user: dict = Depends(get_current_user)):
    """List all content for current user"""
    content_list = db.get_user_content(current_user['id'])
    return {"content": content_list}


# Distribution endpoints
@app.post("/distribute", response_model=PublishResponse)
async def distribute_content(
    request: PublishRequest,
    current_user: dict = Depends(get_current_user)
):
    """Distribute content to selected platforms"""
    content = db.get_content(request.content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create publish job
    job_data = {
        "content_id": request.content_id,
        "platforms": [p.value for p in request.platforms],
        "scheduled_time": request.scheduled_time.isoformat() if request.scheduled_time else None,
        "status": PublishStatus.SCHEDULED.value if request.scheduled_time else PublishStatus.PUBLISHING.value,
        "platform_results": {}
    }
    
    job_id = db.create_publish_job(job_data)
    
    # In production, this would trigger actual platform publishing
    # For now, we'll simulate success
    platform_results = {}
    for platform in request.platforms:
        platform_results[platform.value] = {
            "platform": platform.value,
            "success": True,
            "post_url": f"https://{platform.value}.com/post/{content['id']}",
            "error": None
        }
    
    db.update_publish_job(job_id, {
        "status": PublishStatus.COMPLETED.value,
        "platform_results": platform_results
    })
    
    return PublishResponse(
        job_id=job_id,
        status=PublishStatus.COMPLETED,
        platform_results=platform_results
    )


@app.get("/distribute/{job_id}")
async def get_publish_status(job_id: str, current_user: dict = Depends(get_current_user)):
    """Get publishing job status"""
    job = db.get_publish_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify user owns the content
    content = db.get_content(job['content_id'])
    if content['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return job


# Analytics endpoints
@app.get("/analytics/{content_id}")
async def get_content_analytics(content_id: str, current_user: dict = Depends(get_current_user)):
    """Get analytics for specific content"""
    content = db.get_content(content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Query analytics from DynamoDB
    table = db.get_table('analytics')
    response = table.query(
        IndexName='content-index',
        KeyConditionExpression='content_id = :content_id',
        ExpressionAttributeValues={':content_id': content_id}
    )
    
    return {"content_id": content_id, "analytics": response.get('Items', [])}


@app.post("/analytics/trends")
async def get_trend_predictions(niche: str, current_user: dict = Depends(get_current_user)):
    """Get trend predictions for a niche"""
    # Use Bedrock to analyze trends
    suggestions = bedrock_service.suggest_content_improvements(
        {"niche": niche},
        niche
    )
    
    return TrendPrediction(
        niche=niche,
        trending_topics=suggestions.get('trending_topics', []),
        suggested_hooks=suggestions.get('suggested_hooks', []),
        optimal_posting_times=suggestions.get('posting_times', []),
        shooting_styles=suggestions.get('shooting_styles', []),
        confidence_score=0.85
    )


# Monetization endpoints
@app.post("/monetization/analyze/{content_id}")
async def analyze_monetization(content_id: str, current_user: dict = Depends(get_current_user)):
    """Analyze content for ad placement opportunities"""
    content = db.get_content(content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Trigger ad placement analysis
    task = analyze_ad_placements.delay(content_id)
    
    return {"task_id": task.id, "status": "processing"}


@app.get("/monetization/{content_id}/placements")
async def get_ad_placements(content_id: str, current_user: dict = Depends(get_current_user)):
    """Get ad placements for content"""
    content = db.get_content(content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Query ad placements
    table = db.get_table('ad_placements')
    response = table.query(
        IndexName='content-index',
        KeyConditionExpression='content_id = :content_id',
        ExpressionAttributeValues={':content_id': content_id}
    )
    
    return {"content_id": content_id, "placements": response.get('Items', [])}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
