# Deployment Checklist

Use this checklist to ensure proper setup and deployment of the Creator Dashboard.

## Pre-Deployment

### AWS Account Setup
- [ ] AWS account created
- [ ] AWS CLI installed and configured
- [ ] IAM user created with appropriate permissions
- [ ] Access keys generated and saved securely

### Bedrock Access
- [ ] Navigate to AWS Bedrock console
- [ ] Request model access for Nova 2 Lite
- [ ] Request model access for Nova 2 Omni (Preview)
- [ ] Wait for approval (usually instant)
- [ ] Verify models are available in your region

### Local Environment
- [ ] Docker installed (version 20.10+)
- [ ] Docker Compose installed (version 2.0+)
- [ ] Git installed
- [ ] Text editor/IDE ready
- [ ] Terminal/command line access

## Initial Setup

### Repository Setup
- [ ] Clone repository
- [ ] Navigate to project directory
- [ ] Copy `.env.example` to `.env`
- [ ] Review `.gitignore` to ensure secrets aren't committed

### Environment Configuration
- [ ] Set `AWS_REGION` (e.g., us-east-1)
- [ ] Set `AWS_ACCESS_KEY_ID`
- [ ] Set `AWS_SECRET_ACCESS_KEY`
- [ ] Set unique `S3_BUCKET_NAME`
- [ ] Set `DYNAMODB_TABLE_PREFIX`
- [ ] Generate secure `JWT_SECRET` (use: `openssl rand -hex 32`)
- [ ] Set `USE_LOCALSTACK=false` for production
- [ ] Review all other environment variables

### AWS Infrastructure
- [ ] Run `chmod +x scripts/init-aws.sh`
- [ ] Execute `./scripts/init-aws.sh`
- [ ] Verify S3 bucket created: `aws s3 ls`
- [ ] Verify DynamoDB tables created: `aws dynamodb list-tables`
- [ ] Check bucket CORS configuration
- [ ] Verify bucket versioning enabled

## Docker Deployment

### Build Phase
- [ ] Run `make build` or `docker-compose build`
- [ ] Verify no build errors
- [ ] Check image sizes are reasonable
- [ ] Verify all services built successfully

### Start Services
- [ ] Run `make up` or `docker-compose up -d`
- [ ] Wait for services to start (30-60 seconds)
- [ ] Check all containers running: `docker-compose ps`
- [ ] Verify no containers in "Exit" state

### Service Verification
- [ ] Backend health check: `curl http://localhost:8000/health`
- [ ] Frontend accessible: http://localhost:3000
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] Redis responding: `docker-compose exec redis redis-cli ping`
- [ ] Celery worker running: `docker-compose logs celery-worker`

## Application Testing

### User Registration
- [ ] Navigate to http://localhost:3000
- [ ] Click "Get Started" or "Register"
- [ ] Create test account
- [ ] Verify email validation works
- [ ] Check password requirements enforced

### Authentication
- [ ] Login with test account
- [ ] Verify JWT token received
- [ ] Check token stored properly
- [ ] Test logout functionality
- [ ] Verify protected routes require auth

### Video Upload
- [ ] Prepare test video (MP4, MOV, or AVI)
- [ ] Navigate to Dashboard → Upload tab
- [ ] Enter title and description
- [ ] Drag and drop video file
- [ ] Verify upload progress shown
- [ ] Check upload completes successfully
- [ ] Verify video appears in content list

### Video Processing
- [ ] Check Celery worker logs: `docker-compose logs celery-worker`
- [ ] Verify metadata extraction completed
- [ ] Check S3 for uploaded file: `aws s3 ls s3://your-bucket/uploads/`
- [ ] Wait for adaptation processing
- [ ] Verify adaptations created for all platforms
- [ ] Check thumbnails generated

### Platform Adaptations
- [ ] Navigate to content details
- [ ] Verify 4 adaptations created (YouTube, Instagram, TikTok, Twitter)
- [ ] Check each has correct aspect ratio
- [ ] Verify titles are platform-specific
- [ ] Check descriptions are unique
- [ ] Verify hashtags generated

### API Testing
- [ ] Test health endpoint: `curl http://localhost:8000/health`
- [ ] Test authentication: `curl -X POST http://localhost:8000/auth/login`
- [ ] Test content list: `curl http://localhost:8000/content -H "Authorization: Bearer TOKEN"`
- [ ] Review API documentation at http://localhost:8000/docs
- [ ] Test error responses (401, 404, 500)

## Social Media Integration (Optional)

### YouTube
- [ ] Create Google Cloud project
- [ ] Enable YouTube Data API v3
- [ ] Create OAuth 2.0 credentials
- [ ] Add credentials to `.env`
- [ ] Test connection

### Instagram
- [ ] Create Facebook App
- [ ] Add Instagram Basic Display
- [ ] Get App ID and Secret
- [ ] Add credentials to `.env`
- [ ] Test connection

### TikTok
- [ ] Register TikTok Developer account
- [ ] Create app
- [ ] Get Client Key and Secret
- [ ] Add credentials to `.env`
- [ ] Test connection

### Twitter/X
- [ ] Create Twitter Developer account
- [ ] Create app
- [ ] Get API keys
- [ ] Add credentials to `.env`
- [ ] Test connection

## Production Hardening

### Security
- [ ] Change default JWT_SECRET
- [ ] Use strong passwords
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up VPC (if using EC2)
- [ ] Enable AWS WAF
- [ ] Configure security groups
- [ ] Review IAM permissions (principle of least privilege)

### Monitoring
- [ ] Set up CloudWatch logs
- [ ] Configure log retention
- [ ] Create CloudWatch alarms
- [ ] Set up SNS notifications
- [ ] Configure health checks
- [ ] Enable X-Ray tracing (optional)
- [ ] Set up cost alerts

### Backup & Recovery
- [ ] Enable DynamoDB point-in-time recovery
- [ ] Configure S3 lifecycle policies
- [ ] Set up automated backups
- [ ] Test restore procedures
- [ ] Document recovery steps
- [ ] Create disaster recovery plan

### Performance
- [ ] Configure CloudFront CDN
- [ ] Enable Redis caching
- [ ] Optimize DynamoDB indexes
- [ ] Set up auto-scaling
- [ ] Configure load balancer
- [ ] Test under load

### Scaling
- [ ] Scale Celery workers: `docker-compose up -d --scale celery-worker=4`
- [ ] Configure DynamoDB auto-scaling
- [ ] Set up horizontal pod autoscaling (if using K8s)
- [ ] Test scaling behavior
- [ ] Monitor resource usage

## Post-Deployment

### Documentation
- [ ] Update README with production URLs
- [ ] Document any custom configurations
- [ ] Create runbook for common issues
- [ ] Document backup/restore procedures
- [ ] Create incident response plan

### Team Onboarding
- [ ] Share access credentials securely
- [ ] Provide documentation links
- [ ] Schedule training session
- [ ] Set up communication channels
- [ ] Define support procedures

### Monitoring Setup
- [ ] Configure uptime monitoring
- [ ] Set up error tracking
- [ ] Enable performance monitoring
- [ ] Create dashboards
- [ ] Test alert notifications

### Maintenance
- [ ] Schedule regular updates
- [ ] Plan for dependency updates
- [ ] Set up automated backups
- [ ] Create maintenance windows
- [ ] Document update procedures

## Troubleshooting Checklist

### Services Won't Start
- [ ] Check Docker daemon running
- [ ] Verify port availability (3000, 8000, 6379)
- [ ] Review docker-compose logs
- [ ] Check environment variables
- [ ] Verify AWS credentials

### Upload Fails
- [ ] Check S3 bucket exists
- [ ] Verify S3 permissions
- [ ] Check file size limits
- [ ] Review Celery worker logs
- [ ] Verify FFmpeg installed

### Processing Fails
- [ ] Check Celery worker running
- [ ] Review worker logs
- [ ] Verify Redis connection
- [ ] Check disk space
- [ ] Verify video format supported

### Bedrock Errors
- [ ] Verify model access enabled
- [ ] Check AWS region
- [ ] Review IAM permissions
- [ ] Check API quotas
- [ ] Verify credentials

### Database Errors
- [ ] Verify tables exist
- [ ] Check DynamoDB permissions
- [ ] Review table capacity
- [ ] Check for throttling
- [ ] Verify indexes created

## Success Criteria

- [ ] All services running without errors
- [ ] Users can register and login
- [ ] Videos upload successfully
- [ ] Processing completes within expected time
- [ ] Adaptations generated for all platforms
- [ ] API responds within 200ms
- [ ] No critical errors in logs
- [ ] Health checks passing
- [ ] Monitoring alerts configured
- [ ] Backups running successfully

## Sign-Off

- [ ] Development team approval
- [ ] QA testing completed
- [ ] Security review passed
- [ ] Performance testing passed
- [ ] Documentation complete
- [ ] Stakeholder approval
- [ ] Production deployment approved

---

**Deployment Date**: _______________

**Deployed By**: _______________

**Version**: _______________

**Notes**: _______________
