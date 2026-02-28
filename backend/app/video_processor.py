import ffmpeg
import cv2
import numpy as np
from typing import Dict, Tuple, List
from pathlib import Path
import tempfile
import os


class VideoProcessor:
    """Handle video processing, conversion, and adaptation"""
    
    PLATFORM_SPECS = {
        "youtube": {
            "aspect_ratio": "16:9",
            "max_resolution": (3840, 2160),
            "formats": ["mp4"],
            "max_duration": 43200  # 12 hours
        },
        # Instagram, TikTok, and Twitter specs commented out - not currently in use
        # "instagram": {
        #     "aspect_ratio": "1:1",
        #     "max_resolution": (1080, 1080),
        #     "formats": ["mp4"],
        #     "max_duration": 60
        # },
        # "tiktok": {
        #     "aspect_ratio": "9:16",
        #     "max_resolution": (1080, 1920),
        #     "formats": ["mp4"],
        #     "max_duration": 600  # 10 minutes
        # },
        # "twitter": {
        #     "aspect_ratio": "16:9",
        #     "max_resolution": (1920, 1080),
        #     "formats": ["mp4"],
        #     "max_duration": 140
        # }
    }
    
    @staticmethod
    def get_video_metadata(video_path: str) -> Dict:
        """Extract video metadata using ffprobe"""
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                raise ValueError("No video stream found")
            
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            duration = float(probe['format']['duration'])
            fps = eval(video_stream['r_frame_rate'])
            
            return {
                "duration": int(duration),
                "resolution": f"{width}x{height}",
                "aspect_ratio": f"{width}:{height}",
                "width": width,
                "height": height,
                "file_size": int(probe['format']['size']),
                "codec": video_stream['codec_name'],
                "fps": float(fps),
                "bitrate": int(probe['format'].get('bit_rate', 0))
            }
        except Exception as e:
            raise ValueError(f"Error extracting metadata: {str(e)}")
    
    @staticmethod
    def validate_video_format(video_path: str) -> Tuple[bool, str]:
        """Validate video format and size"""
        try:
            # Check file extension
            ext = Path(video_path).suffix.lower()
            if ext not in ['.mp4', '.mov', '.avi']:
                return False, f"Unsupported format: {ext}. Supported: MP4, MOV, AVI"
            
            # Check file size (max 5GB)
            file_size = os.path.getsize(video_path)
            if file_size > 5 * 1024 * 1024 * 1024:
                return False, "File size exceeds 5GB limit"
            
            # Validate video can be read
            metadata = VideoProcessor.get_video_metadata(video_path)
            
            # Check resolution (max 4K)
            if metadata['width'] > 3840 or metadata['height'] > 2160:
                return False, "Resolution exceeds 4K (3840x2160)"
            
            return True, "Valid video file"
        except Exception as e:
            return False, f"Invalid video file: {str(e)}"
    
    @staticmethod
    def convert_aspect_ratio(input_path: str, output_path: str, target_aspect: str, target_resolution: Tuple[int, int]) -> bool:
        """Convert video to target aspect ratio with intelligent cropping"""
        try:
            width, height = target_resolution
            
            # Get input metadata
            metadata = VideoProcessor.get_video_metadata(input_path)
            input_width = metadata['width']
            input_height = metadata['height']
            
            # Calculate crop parameters for center crop
            input_aspect = input_width / input_height
            target_aspect_ratio = width / height
            
            if input_aspect > target_aspect_ratio:
                # Input is wider, crop width
                new_width = int(input_height * target_aspect_ratio)
                crop_x = (input_width - new_width) // 2
                crop_filter = f"crop={new_width}:{input_height}:{crop_x}:0"
            else:
                # Input is taller, crop height
                new_height = int(input_width / target_aspect_ratio)
                crop_y = (input_height - new_height) // 2
                crop_filter = f"crop={input_width}:{new_height}:0:{crop_y}"
            
            # Apply crop and scale
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.filter(stream, 'crop', crop_filter)
            stream = ffmpeg.filter(stream, 'scale', width, height)
            stream = ffmpeg.output(stream, output_path, 
                                  vcodec='libx264',
                                  acodec='aac',
                                  **{'b:v': '5M', 'b:a': '192k'})
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            return True
        except Exception as e:
            print(f"Error converting aspect ratio: {e}")
            return False
    
    @staticmethod
    def generate_thumbnail(video_path: str, output_path: str, timestamp: float = 1.0) -> bool:
        """Generate thumbnail from video at specified timestamp"""
        try:
            stream = ffmpeg.input(video_path, ss=timestamp)
            stream = ffmpeg.output(stream, output_path, vframes=1, format='image2', vcodec='png')
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return True
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return False
    
    @staticmethod
    def extract_frames(video_path: str, num_frames: int = 10) -> List[np.ndarray]:
        """Extract frames from video for analysis"""
        frames = []
        try:
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Extract frames at regular intervals
            interval = max(1, total_frames // num_frames)
            
            for i in range(0, total_frames, interval):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret:
                    frames.append(frame)
                if len(frames) >= num_frames:
                    break
            
            cap.release()
        except Exception as e:
            print(f"Error extracting frames: {e}")
        
        return frames
    
    @staticmethod
    def adapt_for_platform(input_path: str, platform: str, output_dir: str) -> Dict[str, str]:
        """Adapt video for specific platform"""
        spec = VideoProcessor.PLATFORM_SPECS.get(platform)
        if not spec:
            raise ValueError(f"Unknown platform: {platform}")
        
        # Create output paths
        output_video = os.path.join(output_dir, f"{platform}_video.mp4")
        output_thumb = os.path.join(output_dir, f"{platform}_thumbnail.png")
        
        # Convert video
        success = VideoProcessor.convert_aspect_ratio(
            input_path,
            output_video,
            spec['aspect_ratio'],
            spec['max_resolution']
        )
        
        if not success:
            raise ValueError(f"Failed to convert video for {platform}")
        
        # Generate thumbnail
        VideoProcessor.generate_thumbnail(input_path, output_thumb)
        
        return {
            "video_path": output_video,
            "thumbnail_path": output_thumb
        }
    
    @staticmethod
    def optimize_video_quality(input_path: str, output_path: str, target_bitrate: str = "3M") -> bool:
        """Optimize video quality while maintaining visual fidelity"""
        try:
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(stream, output_path,
                                  vcodec='libx264',
                                  acodec='aac',
                                  preset='medium',
                                  crf=23,
                                  **{'b:v': target_bitrate, 'b:a': '192k'})
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return True
        except Exception as e:
            print(f"Error optimizing video: {e}")
            return False
