import pytest
from app.models import (
    Platform, UploadStatus, AdaptationStatus, PublishStatus,
    UserCreate, ContentUploadResponse, VideoMetadata
)


def test_platform_enum():
    """Test Platform enum values"""
    assert Platform.YOUTUBE.value == "youtube"
    assert Platform.INSTAGRAM.value == "instagram"
    assert Platform.TIKTOK.value == "tiktok"
    assert Platform.TWITTER.value == "twitter"


def test_upload_status_enum():
    """Test UploadStatus enum values"""
    assert UploadStatus.PENDING.value == "pending"
    assert UploadStatus.PROCESSING.value == "processing"
    assert UploadStatus.COMPLETED.value == "completed"
    assert UploadStatus.FAILED.value == "failed"


def test_user_create_model():
    """Test UserCreate model validation"""
    user = UserCreate(
        email="test@example.com",
        username="testuser",
        password="securepassword"
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"


def test_video_metadata_model():
    """Test VideoMetadata model"""
    metadata = VideoMetadata(
        duration=120,
        resolution="1920x1080",
        aspect_ratio="16:9",
        file_size=10485760,
        codec="h264",
        fps=30.0
    )
    assert metadata.duration == 120
    assert metadata.resolution == "1920x1080"
    assert metadata.fps == 30.0


def test_content_upload_response():
    """Test ContentUploadResponse model"""
    response = ContentUploadResponse(
        content_id="test-id",
        upload_url="https://example.com/upload",
        status=UploadStatus.PENDING
    )
    assert response.content_id == "test-id"
    assert response.status == UploadStatus.PENDING
