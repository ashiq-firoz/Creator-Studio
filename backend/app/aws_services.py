import boto3
import json
from typing import Optional, Dict, Any, List
from .config import settings
import base64


class S3Service:
    def __init__(self):
        if settings.use_localstack and settings.localstack_endpoint:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=settings.localstack_endpoint,
                region_name=settings.aws_region,
                aws_access_key_id='test',
                aws_secret_access_key='test'
            )
        else:
            self.s3_client = boto3.client(
                's3',
                region_name=settings.aws_region
            )
        
        self.bucket_name = settings.s3_bucket_name
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except:
            try:
                if settings.aws_region == 'us-east-1':
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                else:
                    self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': settings.aws_region}
                    )
            except Exception as e:
                print(f"Error creating bucket: {e}")
    
    def generate_presigned_upload_url(self, key: str, content_type: str, expires_in: int = 3600) -> str:
        """Generate presigned URL for direct upload"""
        url = self.s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=expires_in
        )
        return url
    
    def generate_presigned_download_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate presigned URL for download"""
        url = self.s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': key
            },
            ExpiresIn=expires_in
        )
        return url
    
    def upload_file(self, file_path: str, key: str, content_type: Optional[str] = None) -> str:
        """Upload file to S3"""
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
        
        self.s3_client.upload_file(file_path, self.bucket_name, key, ExtraArgs=extra_args)
        return f"s3://{self.bucket_name}/{key}"
    
    def download_file(self, key: str, file_path: str):
        """Download file from S3"""
        self.s3_client.download_file(self.bucket_name, key, file_path)
    
    def delete_file(self, key: str):
        """Delete file from S3"""
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)


class BedrockService:
    def __init__(self):
        if settings.use_localstack and settings.localstack_endpoint:
            # LocalStack doesn't support Bedrock, use mock for development
            self.bedrock_runtime = None
        else:
            self.bedrock_runtime = boto3.client(
                'bedrock-runtime',
                region_name=settings.aws_region
            )
        
        self.text_model = settings.bedrock_model_text
        self.vision_model = settings.bedrock_model_vision
    
    def generate_text(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Generate text using Amazon Nova Lite"""
        if not self.bedrock_runtime:
            # Mock response for development
            return f"Generated text for: {prompt[:50]}..."
        
        try:
            request_body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature
                }
            }
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.text_model,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['output']['message']['content'][0]['text']
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""
    
    def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        """Analyze image using Amazon Nova Pro"""
        if not self.bedrock_runtime:
            # Mock response for development
            return f"Image analysis: {prompt[:50]}..."
        
        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            request_body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "image": {
                                    "format": "png",
                                    "source": {"bytes": image_base64}
                                }
                            },
                            {"text": prompt}
                        ]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": 500,
                    "temperature": 0.5
                }
            }
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.vision_model,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['output']['message']['content'][0]['text']
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return ""
    
    def generate_platform_metadata(self, platform: str, video_description: str, duration: int) -> Dict[str, Any]:
        """Generate platform-specific title, description, and hashtags"""
        prompt = f"""Generate optimized content metadata for {platform}:
        
Video description: {video_description}
Duration: {duration} seconds

Please provide:
1. An engaging title (within platform limits)
2. A compelling description with relevant keywords
3. 5-10 relevant hashtags

Format as JSON with keys: title, description, hashtags (array)"""
        
        response = self.generate_text(prompt, max_tokens=300)
        
        try:
            # Try to parse JSON response
            return json.loads(response)
        except:
            # Fallback if JSON parsing fails
            return {
                "title": f"Amazing content for {platform}",
                "description": video_description,
                "hashtags": ["#content", "#viral", "#trending"]
            }
    
    def detect_ad_placements(self, frame_bytes: bytes) -> List[Dict[str, Any]]:
        """Detect suitable surfaces for ad placement in video frame"""
        prompt = """Analyze this video frame and identify flat surfaces or areas suitable for natural ad placement.
        
For each suitable area, provide:
1. Location (x, y coordinates as percentages)
2. Size (width, height as percentages)
3. Confidence score (0-1)
4. Surface type (wall, floor, object, etc.)

Format as JSON array."""
        
        response = self.analyze_image(frame_bytes, prompt)
        
        try:
            placements = json.loads(response)
            return placements if isinstance(placements, list) else []
        except:
            # Fallback mock placement
            return [{
                "x": 10,
                "y": 10,
                "width": 20,
                "height": 15,
                "confidence": 0.85,
                "surface_type": "wall"
            }]
    
    def suggest_content_improvements(self, video_metadata: Dict[str, Any], niche: str) -> Dict[str, Any]:
        """Suggest content improvements based on trends"""
        prompt = f"""Analyze this content and suggest improvements for the {niche} niche:

Metadata: {json.dumps(video_metadata)}

Provide:
1. Trending topics in this niche
2. Suggested hooks and opening lines
3. Optimal video length
4. Best posting times
5. Shooting style recommendations

Format as JSON."""
        
        response = self.generate_text(prompt, max_tokens=500)
        
        try:
            return json.loads(response)
        except:
            return {
                "trending_topics": ["topic1", "topic2"],
                "suggested_hooks": ["hook1", "hook2"],
                "optimal_length": "60-90 seconds",
                "posting_times": ["9 AM", "6 PM"],
                "shooting_styles": ["close-up", "dynamic"]
            }


# Global service instances
s3_service = S3Service()
bedrock_service = BedrockService()
