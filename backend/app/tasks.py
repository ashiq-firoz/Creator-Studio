from celery import Task
from .celery_app import celery_app
from .database import db
from .aws_services import s3_service, bedrock_service
from .video_processor import VideoProcessor
from .models import Platform, AdaptationStatus, UploadStatus
import tempfile
import os
from typing import Dict, Any
from datetime import datetime


class CallbackTask(Task):
    """Base task with callbacks"""
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f"Task {task_id} failed: {exc}")


@celery_app.task(base=CallbackTask, bind=True)
def process_video_upload(self, content_id: str, s3_key: str):
    """Process uploaded video and extract metadata"""
    try:
        # Update status
        db.update_content(content_id, {"upload_status": UploadStatus.PROCESSING.value})
        
        # Download video from S3
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        s3_service.download_file(s3_key, tmp_path)
        
        # Extract metadata
        metadata = VideoProcessor.get_video_metadata(tmp_path)
        
        # Update content with metadata
        db.update_content(content_id, {
            "upload_status": UploadStatus.COMPLETED.value,
            "duration": metadata['duration'],
            "resolution": metadata['resolution'],
            "aspect_ratio": metadata['aspect_ratio'],
            "codec": metadata['codec'],
            "fps": metadata['fps']
        })
        
        # Clean up
        os.unlink(tmp_path)
        
        # Trigger adaptation generation
        generate_platform_adaptations.delay(content_id)
        
        return {"status": "success", "content_id": content_id}
    
    except Exception as e:
        db.update_content(content_id, {"upload_status": UploadStatus.FAILED.value})
        raise


@celery_app.task(base=CallbackTask, bind=True)
def generate_platform_adaptations(self, content_id: str):
    """Generate platform-specific adaptations"""
    try:
        content = db.get_content(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")
        
        s3_key = content['original_file_url'].replace(f"s3://{s3_service.bucket_name}/", "")
        
        # Download original video
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        s3_service.download_file(s3_key, tmp_path)
        
        # Create temp directory for outputs
        output_dir = tempfile.mkdtemp()
        
        # Only YouTube is currently enabled
        platforms = [Platform.YOUTUBE]
        # platforms = [Platform.YOUTUBE, Platform.INSTAGRAM, Platform.TIKTOK, Platform.TWITTER]  # Uncomment when other APIs are configured
        
        for platform in platforms:
            try:
                # Create adaptation record
                adaptation_id = db.create_adaptation({
                    "content_id": content_id,
                    "platform": platform.value,
                    "status": AdaptationStatus.PROCESSING.value
                })
                
                # Adapt video for platform
                adapted_files = VideoProcessor.adapt_for_platform(
                    tmp_path,
                    platform.value,
                    output_dir
                )
                
                # Upload adapted video and thumbnail to S3
                video_key = f"adaptations/{content_id}/{platform.value}/video.mp4"
                thumb_key = f"adaptations/{content_id}/{platform.value}/thumbnail.png"
                
                s3_service.upload_file(adapted_files['video_path'], video_key, 'video/mp4')
                s3_service.upload_file(adapted_files['thumbnail_path'], thumb_key, 'image/png')
                
                # Generate metadata using Bedrock
                metadata = bedrock_service.generate_platform_metadata(
                    platform.value,
                    content.get('description', ''),
                    content.get('duration', 0)
                )
                
                # Update adaptation
                db.get_table('adaptations').update_item(
                    Key={'id': adaptation_id},
                    UpdateExpression="SET #status = :status, adapted_file_url = :video_url, thumbnail_url = :thumb_url, title = :title, description = :desc, hashtags = :tags",
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={
                        ':status': AdaptationStatus.COMPLETED.value,
                        ':video_url': f"s3://{s3_service.bucket_name}/{video_key}",
                        ':thumb_url': f"s3://{s3_service.bucket_name}/{thumb_key}",
                        ':title': metadata.get('title', ''),
                        ':desc': metadata.get('description', ''),
                        ':tags': metadata.get('hashtags', [])
                    }
                )
                
            except Exception as e:
                print(f"Error adapting for {platform.value}: {e}")
                db.get_table('adaptations').update_item(
                    Key={'id': adaptation_id},
                    UpdateExpression="SET #status = :status",
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={':status': AdaptationStatus.FAILED.value}
                )
        
        # Clean up
        os.unlink(tmp_path)
        import shutil
        shutil.rmtree(output_dir)
        
        return {"status": "success", "content_id": content_id}
    
    except Exception as e:
        print(f"Error generating adaptations: {e}")
        raise


@celery_app.task(base=CallbackTask, bind=True)
def analyze_ad_placements(self, content_id: str):
    """Analyze video for ad placement opportunities"""
    try:
        content = db.get_content(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")
        
        s3_key = content['original_file_url'].replace(f"s3://{s3_service.bucket_name}/", "")
        
        # Download video
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        s3_service.download_file(s3_key, tmp_path)
        
        # Extract frames for analysis
        frames = VideoProcessor.extract_frames(tmp_path, num_frames=5)
        
        placements = []
        for idx, frame in enumerate(frames):
            # Convert frame to bytes
            import cv2
            _, buffer = cv2.imencode('.png', frame)
            frame_bytes = buffer.tobytes()
            
            # Analyze frame for ad placements
            frame_placements = bedrock_service.detect_ad_placements(frame_bytes)
            
            for placement in frame_placements:
                placement_data = {
                    "content_id": content_id,
                    "frame_number": idx,
                    "x": placement.get('x', 0),
                    "y": placement.get('y', 0),
                    "width": placement.get('width', 0),
                    "height": placement.get('height', 0),
                    "confidence": placement.get('confidence', 0),
                    "surface_type": placement.get('surface_type', 'unknown')
                }
                
                placement_id = db.get_table('ad_placements').put_item(Item=placement_data)
                placements.append(placement_data)
        
        # Clean up
        os.unlink(tmp_path)
        
        return {"status": "success", "placements_found": len(placements)}
    
    except Exception as e:
        print(f"Error analyzing ad placements: {e}")
        raise


@celery_app.task(base=CallbackTask, bind=True)
def collect_analytics(self, content_id: str):
    """Collect analytics from all platforms"""
    try:
        # This would integrate with actual platform APIs
        # For now, we'll create a placeholder
        
        content = db.get_content(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")
        
        # Get all adaptations
        adaptations = db.get_content_adaptations(content_id)
        
        for adaptation in adaptations:
            # Simulate collecting metrics
            # In production, this would call platform APIs
            metrics = {
                "content_id": content_id,
                "platform": adaptation['platform'],
                "views": 0,
                "likes": 0,
                "shares": 0,
                "comments": 0,
                "engagement_rate": 0.0,
                "collected_at": datetime.utcnow().isoformat()
            }
            
            db.get_table('analytics').put_item(Item=metrics)
        
        return {"status": "success", "content_id": content_id}
    
    except Exception as e:
        print(f"Error collecting analytics: {e}")
        raise


# Periodic tasks
@celery_app.task
def periodic_analytics_collection():
    """Periodically collect analytics for all published content"""
    # This would be scheduled to run every 15 minutes
    # Implementation would query all published content and collect metrics
    pass


@celery_app.task
def cleanup_old_files():
    """Clean up old temporary files and expired content"""
    # Implementation for cleanup tasks
    pass
