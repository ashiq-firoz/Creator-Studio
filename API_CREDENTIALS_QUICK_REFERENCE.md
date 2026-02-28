# API Credentials Quick Reference

Quick links and key information for obtaining social media API credentials.

## 📺 YouTube API

**Portal**: https://console.cloud.google.com/

**Steps**:
1. Create Google Cloud Project
2. Enable YouTube Data API v3
3. Create OAuth 2.0 Client ID
4. Configure consent screen
5. Copy Client ID and Secret

**What you need**:
- `YOUTUBE_CLIENT_ID` - Looks like: `123456789-abc...apps.googleusercontent.com`
- `YOUTUBE_CLIENT_SECRET` - Looks like: `GOCSPX-abc123...`

**Cost**: Free (10,000 units/day quota)

**Time**: ~10 minutes

---

## 📸 Instagram API

**Portal**: https://developers.facebook.com/

**Steps**:
1. Convert Instagram to Business account
2. Create Facebook Page
3. Connect Instagram to Facebook Page
4. Create Facebook App
5. Add Instagram Basic Display & Graph API
6. Copy App ID and Secret

**What you need**:
- `INSTAGRAM_APP_ID` - Numeric ID like: `123456789012345`
- `INSTAGRAM_APP_SECRET` - String like: `abc123def456...`

**Cost**: Free (200 calls/hour)

**Time**: ~15 minutes

---

## 🐦 Twitter/X API

**Portal**: https://developer.twitter.com/

**Steps**:
1. Apply for Developer Account
2. Choose access tier (Basic $100/mo for posting)
3. Create Project and App
4. Generate API Keys
5. Configure OAuth 2.0 settings
6. Copy API Key and Secret

**What you need**:
- `TWITTER_API_KEY` - String like: `abc123def456...`
- `TWITTER_API_SECRET` - String like: `abc123def456ghi789...`

**Cost**: 
- Free tier: Very limited (read-only)
- Basic: $100/month (needed for posting)
- Pro: $5,000/month

**Time**: ~10 minutes

---

## 🎵 TikTok API (Not Covered)

**Portal**: https://developers.tiktok.com/

**Note**: TikTok API access is more restricted and requires business verification. The process can take several weeks.

**Steps**:
1. Register as TikTok Developer
2. Submit business verification
3. Wait for approval (can take weeks)
4. Create app
5. Request API access

---

## Quick Setup Checklist

- [ ] YouTube credentials obtained
- [ ] Instagram credentials obtained  
- [ ] Twitter credentials obtained
- [ ] All credentials added to `.env` file
- [ ] Services restarted: `make down && make up`
- [ ] Credentials tested via API calls

---

## Testing Your Credentials

### Test YouTube
```bash
curl "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Test Instagram
```bash
curl "https://graph.instagram.com/me?fields=id,username&access_token=YOUR_ACCESS_TOKEN"
```

### Test Twitter
```bash
curl "https://api.twitter.com/2/users/me" \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

---

## Common Issues

### YouTube
- ❌ "Access Not Configured" → Enable YouTube Data API v3
- ❌ "Invalid Credentials" → Regenerate OAuth credentials
- ❌ "Quota Exceeded" → Wait 24 hours or request increase

### Instagram
- ❌ "Invalid OAuth token" → Regenerate access token
- ❌ "Permissions error" → Request `instagram_content_publish`
- ❌ "Account not connected" → Link Instagram to Facebook Page

### Twitter
- ❌ "Forbidden" → Check API tier and permissions
- ❌ "Rate limit exceeded" → Upgrade tier or wait
- ❌ "Invalid token" → Regenerate access tokens

---

## Security Reminders

✅ Never commit `.env` to Git
✅ Use different credentials for dev/prod
✅ Rotate credentials every 90 days
✅ Monitor API usage regularly
✅ Revoke unused tokens

---

## Full Documentation

For detailed step-by-step instructions with screenshots and troubleshooting:

👉 **[SOCIAL_MEDIA_API_SETUP.md](SOCIAL_MEDIA_API_SETUP.md)**

---

## Support Resources

- **YouTube**: https://developers.google.com/youtube/v3
- **Instagram**: https://developers.facebook.com/docs/instagram-api
- **Twitter**: https://developer.twitter.com/en/docs
- **Application Logs**: `make logs`

---

## Your Credentials Template

Copy this to your `.env` file:

```bash
# YouTube API
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=

# Instagram API  
INSTAGRAM_APP_ID=
INSTAGRAM_APP_SECRET=

# Twitter/X API
TWITTER_API_KEY=
TWITTER_API_SECRET=

# TikTok API (optional)
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
```

After filling in, restart: `make down && make up`
