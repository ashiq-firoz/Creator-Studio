import pytest
from app.video_processor import VideoProcessor
import tempfile
import os


def test_platform_specs():
    """Test that platform specifications are defined - currently only YouTube"""
    assert "youtube" in VideoProcessor.PLATFORM_SPECS
    # Instagram, TikTok, and Twitter are commented out
    # assert "instagram" in VideoProcessor.PLATFORM_SPECS
    # assert "tiktok" in VideoProcessor.PLATFORM_SPECS
    # assert "twitter" in VideoProcessor.PLATFORM_SPECS


def test_youtube_specs():
    """Test YouTube platform specifications"""
    youtube = VideoProcessor.PLATFORM_SPECS["youtube"]
    assert youtube["aspect_ratio"] == "16:9"
    assert youtube["max_resolution"] == (3840, 2160)


# Instagram, TikTok, and Twitter tests commented out - platforms not currently enabled
# def test_instagram_specs():
#     """Test Instagram platform specifications"""
#     instagram = VideoProcessor.PLATFORM_SPECS["instagram"]
#     assert instagram["aspect_ratio"] == "1:1"
#     assert instagram["max_resolution"] == (1080, 1080)


# def test_tiktok_specs():
#     """Test TikTok platform specifications"""
#     tiktok = VideoProcessor.PLATFORM_SPECS["tiktok"]
#     assert tiktok["aspect_ratio"] == "9:16"
#     assert tiktok["max_resolution"] == (1080, 1920)


def test_validate_video_format_invalid_extension():
    """Test video format validation with invalid extension"""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        valid, message = VideoProcessor.validate_video_format(tmp_path)
        assert not valid
        assert "Unsupported format" in message
    finally:
        os.unlink(tmp_path)


def test_validate_video_format_nonexistent():
    """Test video format validation with nonexistent file"""
    valid, message = VideoProcessor.validate_video_format("/nonexistent/file.mp4")
    assert not valid
