# Social Media API Setup Guide

This guide walks you through obtaining API credentials for YouTube, Instagram, and Twitter/X to enable content distribution features.

## Table of Contents
1. [YouTube API Setup](#youtube-api-setup)
2. [Instagram API Setup](#instagram-api-setup)
3. [Twitter/X API Setup](#twitterx-api-setup)
4. [Testing Your Credentials](#testing-your-credentials)

---

## YouTube API Setup

### Prerequisites
- Google account
- Time required: ~10 minutes

### Step-by-Step Instructions

#### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter project details:
   - **Project name**: `Creator Dashboard` (or your preferred name)
   - **Organization**: Leave as default or select your organization
5. Click "Create"
6. Wait for the project to be created (takes a few seconds)

#### 2. Enable YouTube Data API v3

1. In the Google Cloud Console, ensure your new project is selected
2. Go to **APIs & Services** → **Library** (or visit https://console.cloud.google.com/apis/library)
3. Search for "YouTube Data API v3"
4. Click on "YouTube Data API v3"
5. Click the "Enable" button
6. Wait for the API to be enabled

#### 3. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials** (or visit https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" at the top
3. Select "OAuth client ID"

#### 4. Configure OAuth Consent Screen (First Time Only)

If prompted to configure the consent screen:

1. Click "Configure Consent Screen"
2. Choose **External** (unless you have a Google Workspace)
3. Click "Create"
4. Fill in the required fields:
   - **App name**: `Creator Dashboard`
   - **User support email**: Your email
   - **Developer contact email**: Your email
5. Click "Save and Continue"
6. On "Scopes" page, click "Add or Remove Scopes"
7. Add these scopes:
   - `https://www.googleapis.com/auth/youtube.upload`
   - `https://www.googleapis.com/auth/youtube`
   - `https://www.googleapis.com/auth/youtube.force-ssl`
8. Click "Update" then "Save and Continue"
9. On "Test users" page, add your email as a test user
10. Click "Save and Continue"
11. Review and click "Back to Dashboard"

#### 5. Create OAuth Client ID

1. Go back to **Credentials** page
2. Click "Create Credentials" → "OAuth client ID"
3. Select application type: **Web application**
4. Enter name: `Creator Dashboard Web Client`
5. Add Authorized redirect URIs:
   ```
   http://localhost:8000/auth/youtube/callback
   http://localhost:3000/auth/youtube/callback
   ```
   (Add your production URLs when deploying)
6. Click "Create"

#### 6. Save Your Credentials

A popup will show your credentials:
- **Client ID**: Starts with something like `123456789-abc...apps.googleusercontent.com`
- **Client Secret**: A random string like `GOCSPX-abc123...`

**Copy these values immediately!**

Add to your `.env` file:
```bash
YOUTUBE_CLIENT_ID=your_client_id_here
YOUTUBE_CLIENT_SECRET=your_client_secret_here
```

#### 7. Important Notes

- **Quota Limits**: Free tier has 10,000 units/day (1 upload = ~1,600 units)
- **Verification**: For production, you'll need to verify your app (can take weeks)
- **Test Mode**: You can use test mode with up to 100 test users without verification

---

## Instagram API Setup

### Prerequisites
- Facebook account
- Instagram Business or Creator account
- Time required: ~15 minutes

### Step-by-Step Instructions

#### 1. Convert Instagram to Business Account

1. Open Instagram app on your phone
2. Go to your profile
3. Tap the menu (three lines) → Settings
4. Tap "Account"
5. Tap "Switch to Professional Account"
6. Choose "Business" or "Creator"
7. Complete the setup

#### 2. Create a Facebook Page (if you don't have one)

1. Go to [Facebook](https://www.facebook.com/)
2. Click "Pages" in the left menu
3. Click "Create New Page"
4. Enter page details:
   - **Page name**: Your brand name
   - **Category**: Choose relevant category
5. Click "Create Page"

#### 3. Connect Instagram to Facebook Page

1. Go to your Facebook Page
2. Click "Settings" in the left menu
3. Click "Instagram" in the left sidebar
4. Click "Connect Account"
5. Log in to your Instagram account
6. Authorize the connection

#### 4. Create a Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click "My Apps" in the top right
3. Click "Create App"
4. Choose app type: **Business**
5. Click "Next"
6. Fill in app details:
   - **App name**: `Creator Dashboard`
   - **App contact email**: Your email
7. Click "Create App"
8. Complete security check if prompted

#### 5. Add Instagram Basic Display

1. In your app dashboard, scroll down to "Add Products"
2. Find "Instagram Basic Display" and click "Set Up"
3. Click "Create New App"
4. Fill in:
   - **Display Name**: `Creator Dashboard`
   - **Valid OAuth Redirect URIs**: 
     ```
     http://localhost:8000/auth/instagram/callback
     http://localhost:3000/auth/instagram/callback
     ```
   - **Deauthorize Callback URL**: `http://localhost:8000/auth/instagram/deauthorize`
   - **Data Deletion Request URL**: `http://localhost:8000/auth/instagram/delete`
5. Click "Save Changes"

#### 6. Add Instagram Graph API (for posting)

1. Go back to your app dashboard
2. Click "Add Products"
3. Find "Instagram Graph API" and click "Set Up"
4. This allows you to post content programmatically

#### 7. Get Your Credentials

1. In the left sidebar, click "Settings" → "Basic"
2. You'll see:
   - **App ID**: A numeric ID (e.g., 123456789012345)
   - **App Secret**: Click "Show" to reveal (e.g., abc123def456...)

**Copy these values!**

Add to your `.env` file:
```bash
INSTAGRAM_APP_ID=your_app_id_here
INSTAGRAM_APP_SECRET=your_app_secret_here
```

#### 8. Add Test Users (Development)

1. Go to "Roles" → "Instagram Testers"
2. Click "Add Instagram Testers"
3. Enter Instagram username
4. The user must accept the invitation in their Instagram app

#### 9. Important Notes

- **Permissions**: You'll need to request permissions for `instagram_content_publish`
- **Review**: For production, submit your app for review
- **Rate Limits**: 200 calls per hour per user
- **Content Types**: Supports photos, videos, carousels, and stories

---

## Twitter/X API Setup

### Prerequisites
- Twitter/X account (must be verified with phone number)
- Time required: ~10 minutes
- Note: Twitter API now requires paid access for most features

### Step-by-Step Instructions

#### 1. Apply for Developer Account

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Click "Sign up" or "Apply" in the top right
3. Log in with your Twitter account
4. Click "Apply for a developer account"

#### 2. Choose Access Level

Twitter now has tiered access:
- **Free**: Very limited (1,500 tweets/month read, no write access)
- **Basic**: $100/month (3,000 tweets/month, 50 posts/month)
- **Pro**: $5,000/month (Full access)

For the Creator Dashboard, you'll need at least **Basic** tier for posting.

#### 3. Complete Application

1. Select "Hobbyist" or "Professional" use case
2. Describe your use case:
   ```
   Building a content management dashboard that helps creators 
   distribute their content across multiple social media platforms 
   including Twitter. The app will post videos and text content 
   on behalf of authenticated users.
   ```
3. Answer all required questions
4. Agree to terms and conditions
5. Verify your email address
6. Wait for approval (usually instant for basic tier)

#### 4. Create a Project and App

1. Once approved, go to the [Developer Portal Dashboard](https://developer.twitter.com/en/portal/dashboard)
2. Click "Create Project"
3. Fill in project details:
   - **Project name**: `Creator Dashboard`
   - **Use case**: Choose relevant option
   - **Project description**: Brief description of your app
4. Click "Next"
5. Create an App:
   - **App name**: `creator-dashboard-app` (must be unique)
   - **Environment**: Development or Production
6. Click "Complete"

#### 5. Get Your API Keys

After creating the app, you'll see:
- **API Key** (also called Consumer Key)
- **API Key Secret** (also called Consumer Secret)
- **Bearer Token**

**Copy these immediately!** You can only see them once.

Add to your `.env` file:
```bash
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_key_secret_here
```

#### 6. Configure App Settings

1. In your app dashboard, click "Settings"
2. Scroll to "User authentication settings"
3. Click "Set up"
4. Configure OAuth 2.0:
   - **App permissions**: Read and Write
   - **Type of App**: Web App
   - **Callback URI**: 
     ```
     http://localhost:8000/auth/twitter/callback
     http://localhost:3000/auth/twitter/callback
     ```
   - **Website URL**: Your website or `http://localhost:3000`
5. Click "Save"

#### 7. Generate Access Token and Secret

1. Go to "Keys and tokens" tab
2. Under "Authentication Tokens", click "Generate"
3. You'll get:
   - **Access Token**
   - **Access Token Secret**

**Save these as well!** (Optional, for app-level access)

#### 8. Important Notes

- **Pricing**: Free tier is very limited; Basic ($100/mo) needed for posting
- **Rate Limits**: Vary by tier
- **Media Upload**: Supported for images and videos
- **Character Limit**: 280 characters (or 4,000 for Twitter Blue)
- **API Version**: Use v2 API for best features

---

## Testing Your Credentials

### Test YouTube Credentials

```bash
# Using curl
curl "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Test Instagram Credentials

```bash
# Get user info
curl "https://graph.instagram.com/me?fields=id,username&access_token=YOUR_ACCESS_TOKEN"
```

### Test Twitter Credentials

```bash
# Get user info
curl "https://api.twitter.com/2/users/me" \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

### Test in Your Application

1. Update your `.env` file with all credentials
2. Restart your Docker containers:
   ```bash
   make down
   make up
   ```
3. Check logs for any authentication errors:
   ```bash
   make logs
   ```

---

## Complete .env Example

After obtaining all credentials, your `.env` should look like:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3_BUCKET_NAME=creator-dashboard-videos
DYNAMODB_TABLE_PREFIX=creator-dashboard

# Bedrock Models
BEDROCK_MODEL_TEXT=us.amazon.nova-lite-v1:0
BEDROCK_MODEL_VISION=us.amazon.nova-pro-v1:0

# Security
JWT_SECRET=your_generated_secret_key_here

# Redis
REDIS_URL=redis://redis:6379

# YouTube API
YOUTUBE_CLIENT_ID=123456789-abc123.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=GOCSPX-abc123def456

# Instagram API
INSTAGRAM_APP_ID=123456789012345
INSTAGRAM_APP_SECRET=abc123def456ghi789

# Twitter/X API
TWITTER_API_KEY=abc123def456ghi789jkl
TWITTER_API_SECRET=abc123def456ghi789jkl012mno345pqr678stu

# LocalStack (for development)
USE_LOCALSTACK=false
```

---

## Troubleshooting

### YouTube Issues

**Error: "Access Not Configured"**
- Solution: Make sure YouTube Data API v3 is enabled in Google Cloud Console

**Error: "Invalid Credentials"**
- Solution: Regenerate OAuth credentials and update .env file

**Error: "Quota Exceeded"**
- Solution: Wait 24 hours or request quota increase in Google Cloud Console

### Instagram Issues

**Error: "Invalid OAuth access token"**
- Solution: Regenerate access token or check token expiration

**Error: "Permissions error"**
- Solution: Ensure you've requested and been granted `instagram_content_publish` permission

**Error: "Instagram account not connected"**
- Solution: Connect Instagram Business account to Facebook Page

### Twitter Issues

**Error: "Forbidden"**
- Solution: Check your API access tier and ensure you have write permissions

**Error: "Rate limit exceeded"**
- Solution: Implement rate limiting in your app or upgrade tier

**Error: "Invalid or expired token"**
- Solution: Regenerate access tokens

---

## Security Best Practices

1. **Never commit credentials to Git**
   - Always use `.env` file
   - Ensure `.env` is in `.gitignore`

2. **Rotate credentials regularly**
   - Change API keys every 90 days
   - Revoke unused tokens

3. **Use environment-specific credentials**
   - Different keys for development and production
   - Separate test accounts

4. **Monitor API usage**
   - Set up alerts for unusual activity
   - Track quota usage

5. **Implement OAuth flows properly**
   - Use state parameter to prevent CSRF
   - Validate redirect URIs
   - Store tokens securely

---

## Next Steps

After setting up all credentials:

1. ✅ Update `.env` file with all API keys
2. ✅ Restart your application: `make down && make up`
3. ✅ Test authentication flows for each platform
4. ✅ Implement OAuth callback handlers in your backend
5. ✅ Test content posting to each platform
6. ✅ Monitor API usage and rate limits

---

## Additional Resources

### YouTube
- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [OAuth 2.0 Guide](https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps)
- [Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)

### Instagram
- [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Content Publishing Guide](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)

### Twitter/X
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [API v2 Guide](https://developer.twitter.com/en/docs/twitter-api)
- [Media Upload Guide](https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/overview)

---

## Support

If you encounter issues:
1. Check the official documentation for each platform
2. Review error messages in application logs: `make logs`
3. Verify credentials are correctly set in `.env`
4. Ensure all required permissions are granted
5. Check API status pages for outages

Good luck with your API setup! 🚀
