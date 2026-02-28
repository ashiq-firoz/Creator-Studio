from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum
from decimal import Decimal


class Platform(str, Enum):
    YOUTUBE = "youtube"
    # INSTAGRAM = "instagram"  # Commented out - API credentials not configured
    # TIKTOK = "tiktok"  # Commented out - API credentials not configured
    # TWITTER = "twitter"  # Commented out - API credentials not configured


class UploadStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AdaptationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class PublishStatus(str, Enum):
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


# Request/Response Models
class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    subscription_tier: SubscriptionTier
    connected_platforms: List[Platform]
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ContentUploadResponse(BaseModel):
    content_id: str
    upload_url: str
    status: UploadStatus


class VideoMetadata(BaseModel):
    duration: int
    resolution: str
    aspect_ratio: str
    file_size: int
    codec: str
    fps: float


class PlatformAdaptation(BaseModel):
    id: str
    content_id: str
    platform: Platform
    adapted_file_url: str
    thumbnail_url: str
    title: str
    description: str
    hashtags: List[str]
    aspect_ratio: str
    status: AdaptationStatus


class PublishRequest(BaseModel):
    content_id: str
    platforms: List[Platform]
    scheduled_time: Optional[datetime] = None
    immediate: bool = False


class PublishResult(BaseModel):
    platform: Platform
    success: bool
    post_url: Optional[str] = None
    error: Optional[str] = None


class PublishResponse(BaseModel):
    job_id: str
    status: PublishStatus
    platform_results: Dict[str, PublishResult]


class AnalyticsMetrics(BaseModel):
    content_id: str
    platform: Platform
    views: int
    likes: int
    shares: int
    comments: int
    engagement_rate: float
    collected_at: datetime


class TrendPrediction(BaseModel):
    niche: str
    trending_topics: List[str]
    suggested_hooks: List[str]
    optimal_posting_times: List[str]
    shooting_styles: List[str]
    confidence_score: float


class AdPlacementCoordinates(BaseModel):
    frame_number: int
    x: int
    y: int
    width: int
    height: int
    confidence: float


class AdPlacement(BaseModel):
    id: str
    content_id: str
    placement_coordinates: AdPlacementCoordinates
    ad_type: str
    brand_id: str
    revenue_generated: Decimal
    placement_effectiveness: float
    created_at: datetime


class AdPlacementRequest(BaseModel):
    content_id: str
    brand_id: str
    ad_type: str
    max_placements: int = 3


class RevenueReport(BaseModel):
    user_id: str
    total_revenue: Decimal
    placements_count: int
    average_effectiveness: float
    timeframe_start: datetime
    timeframe_end: datetime
    breakdown_by_content: Dict[str, Decimal]
