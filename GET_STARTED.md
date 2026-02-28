# 🚀 Get Started with Creator Dashboard

Welcome! This guide will get you up and running in 3 simple steps.

## Choose Your Path

### 🏃 Fast Track (5 minutes)
Just want to see it work? Skip social media APIs for now.

### 🎯 Full Setup (30 minutes)
Get everything working including social media distribution.

---

## 🏃 Fast Track Setup

Perfect for testing and development without social media integration.

### Step 1: Clone & Configure (2 min)

```bash
# Clone the repository
git clone <repository-url>
cd creator-dashboard

# Copy environment file
cp .env.example .env

# Edit .env - set USE_LOCALSTACK=true for local testing
```

### Step 2: Start Services (2 min)

```bash
# Build and start
make build
make up

# Wait about 30 seconds for services to start
```

### Step 3: Access & Test (1 min)

Open your browser:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

Create an account and upload a test video!

**Note**: Without social media APIs, you can still:
- ✅ Upload videos
- ✅ Generate platform adaptations
- ✅ See AI-generated metadata
- ✅ Test the full interface
- ❌ Can't actually post to social media

---

## 🎯 Full Setup with Social Media

Get the complete experience with real social media posting.

### Step 1: Get AWS Credentials (10 min)

1. Create AWS account at https://aws.amazon.com
2. Go to IAM → Users → Create User
3. Attach policies:
   - AmazonS3FullAccess
   - AmazonDynamoDBFullAccess
   - AmazonBedrockFullAccess
4. Create access key
5. Save Access Key ID and Secret Access Key

### Step 2: Enable Bedrock Models (5 min)

1. Go to AWS Console → Amazon Bedrock
2. Click "Model access" in sidebar
3. Click "Manage model access"
4. Enable:
   - ✅ Amazon Nova Lite
   - ✅ Amazon Nova Pro (preview)
5. Click "Save changes"

### Step 3: Get Social Media APIs (15 min)

Choose which platforms you want:

#### YouTube (Required for YouTube posting)
- Time: 10 minutes
- Cost: Free
- Guide: [SOCIAL_MEDIA_API_SETUP.md#youtube-api-setup](SOCIAL_MEDIA_API_SETUP.md#youtube-api-setup)

#### Instagram (Required for Instagram posting)
- Time: 15 minutes
- Cost: Free
- Guide: [SOCIAL_MEDIA_API_SETUP.md#instagram-api-setup](SOCIAL_MEDIA_API_SETUP.md#instagram-api-setup)

#### Twitter/X (Required for Twitter posting)
- Time: 10 minutes
- Cost: $100/month for posting (Free tier is read-only)
- Guide: [SOCIAL_MEDIA_API_SETUP.md#twitterx-api-setup](SOCIAL_MEDIA_API_SETUP.md#twitterx-api-setup)

**Quick Reference**: [API_CREDENTIALS_QUICK_REFERENCE.md](API_CREDENTIALS_QUICK_REFERENCE.md)

### Step 4: Configure Environment

Edit your `.env` file:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
S3_BUCKET_NAME=creator-dashboard-videos-unique-name
DYNAMODB_TABLE_PREFIX=creator-dashboard

# Disable LocalStack for production
USE_LOCALSTACK=false

# Generate a secure JWT secret
JWT_SECRET=$(openssl rand -hex 32)

# Add your social media credentials
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
INSTAGRAM_APP_ID=your_instagram_app_id
INSTAGRAM_APP_SECRET=your_instagram_app_secret
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
```

### Step 5: Initialize AWS Infrastructure

```bash
# Create S3 bucket and DynamoDB tables
make init-aws

# This creates:
# - S3 bucket with versioning
# - 6 DynamoDB tables with indexes
```

### Step 6: Deploy

```bash
# Build and start all services
make build
make up

# Check everything is running
make logs
```

### Step 7: Test Everything

1. Go to http://localhost:3000
2. Register a new account
3. Upload a test video
4. Wait for processing (check logs: `make logs`)
5. View generated adaptations
6. Try distributing to platforms!

---

## 📚 Documentation Map

Depending on what you need:

### Getting Started
- **This file** - Quick start guide
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
- [API_CREDENTIALS_QUICK_REFERENCE.md](API_CREDENTIALS_QUICK_REFERENCE.md) - Quick API reference

### Setup Guides
- [SOCIAL_MEDIA_API_SETUP.md](SOCIAL_MEDIA_API_SETUP.md) - Detailed API credential guide
- [CHECKLIST.md](CHECKLIST.md) - Complete deployment checklist

### Technical Documentation
- [README.md](README.md) - Main documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [SYSTEM_FLOW.md](SYSTEM_FLOW.md) - Visual diagrams
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File organization

### Deployment
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What was built

---

## 🎯 What Can You Do?

### Without Social Media APIs
✅ Upload videos (MP4, MOV, AVI)
✅ Automatic video processing
✅ Generate 4 platform versions (YouTube, Instagram, TikTok, Twitter)
✅ AI-generated titles and descriptions
✅ Custom thumbnails per platform
✅ View all adaptations
✅ Test the complete interface

### With Social Media APIs
✅ Everything above, PLUS:
✅ Actually post to YouTube
✅ Actually post to Instagram
✅ Actually post to Twitter/X
✅ Schedule posts
✅ Track real analytics
✅ Multi-platform distribution

---

## 🆘 Need Help?

### Common Issues

**Services won't start**
```bash
# Check Docker is running
docker ps

# Rebuild everything
make clean
make build
make up
```

**Can't access frontend**
- Check http://localhost:3000 is not blocked
- Check logs: `make logs`
- Verify port 3000 is not in use

**Video upload fails**
- Check Celery worker is running: `docker-compose ps`
- View worker logs: `docker-compose logs celery-worker`
- Verify FFmpeg is installed: `docker-compose exec backend ffmpeg -version`

**AWS/Bedrock errors**
- Verify credentials in `.env`
- Check Bedrock model access is enabled
- Ensure you're in a supported region (us-east-1, us-west-2)

### Get More Help

1. Check the logs: `make logs`
2. Review [TROUBLESHOOTING.md](SOCIAL_MEDIA_API_SETUP.md#troubleshooting)
3. Check API documentation for each platform
4. Open an issue on GitHub

---

## 🎉 Next Steps

Once everything is running:

1. **Upload your first video**
   - Go to Dashboard → Upload
   - Drag and drop a video
   - Add title and description

2. **Review adaptations**
   - Check the generated versions
   - Review AI-generated metadata
   - Preview thumbnails

3. **Test distribution**
   - Select platforms
   - Schedule or post immediately
   - Track status

4. **Explore features**
   - Analytics dashboard
   - Monetization options
   - Content management

---

## 💡 Pro Tips

1. **Start with LocalStack** for free local testing
2. **Get YouTube API first** - it's the easiest
3. **Test with short videos** initially (under 1 minute)
4. **Monitor your AWS costs** with budget alerts
5. **Use test accounts** for social media during development

---

## 🚀 Ready to Deploy to Production?

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Production configuration
- Security hardening
- Scaling strategies
- Monitoring setup
- Backup procedures

---

## 📊 System Requirements

### Development
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### Production
- AWS account
- 8GB RAM recommended
- 50GB+ disk space
- Domain name (optional)

---

## 🎬 You're All Set!

Choose your path above and start building! 

Questions? Check the documentation or open an issue.

Happy creating! 🎥✨
