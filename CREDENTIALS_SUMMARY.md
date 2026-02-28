# Social Media API Credentials - Summary

## What You Need

To enable full social media distribution, you need API credentials from three platforms:

### 1. YouTube (Google Cloud)
- **YOUTUBE_CLIENT_ID** - OAuth Client ID
- **YOUTUBE_CLIENT_SECRET** - OAuth Client Secret
- **Time**: 10 minutes
- **Cost**: Free (10,000 API units/day)
- **Difficulty**: Easy ⭐

### 2. Instagram (Facebook/Meta)
- **INSTAGRAM_APP_ID** - Facebook App ID
- **INSTAGRAM_APP_SECRET** - Facebook App Secret
- **Time**: 15 minutes
- **Cost**: Free (200 calls/hour)
- **Difficulty**: Medium ⭐⭐

### 3. Twitter/X
- **TWITTER_API_KEY** - API Key (Consumer Key)
- **TWITTER_API_SECRET** - API Secret (Consumer Secret)
- **Time**: 10 minutes
- **Cost**: $100/month for posting (Free tier is read-only)
- **Difficulty**: Easy ⭐

---

## Quick Links

### YouTube
🔗 **Portal**: https://console.cloud.google.com/
📖 **Guide**: [SOCIAL_MEDIA_API_SETUP.md#youtube-api-setup](SOCIAL_MEDIA_API_SETUP.md#youtube-api-setup)

**Quick Steps**:
1. Create Google Cloud Project
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Copy Client ID and Secret

### Instagram
🔗 **Portal**: https://developers.facebook.com/
📖 **Guide**: [SOCIAL_MEDIA_API_SETUP.md#instagram-api-setup](SOCIAL_MEDIA_API_SETUP.md#instagram-api-setup)

**Quick Steps**:
1. Convert Instagram to Business account
2. Create Facebook Page and connect Instagram
3. Create Facebook App
4. Add Instagram Basic Display & Graph API
5. Copy App ID and Secret

### Twitter/X
🔗 **Portal**: https://developer.twitter.com/
📖 **Guide**: [SOCIAL_MEDIA_API_SETUP.md#twitterx-api-setup](SOCIAL_MEDIA_API_SETUP.md#twitterx-api-setup)

**Quick Steps**:
1. Apply for Developer Account
2. Choose Basic tier ($100/mo for posting)
3. Create Project and App
4. Generate API Keys
5. Copy API Key and Secret

---

## Where to Put Credentials

Add all credentials to your `.env` file:

```bash
# YouTube API
YOUTUBE_CLIENT_ID=123456789-abc...apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=GOCSPX-abc123...

# Instagram API
INSTAGRAM_APP_ID=123456789012345
INSTAGRAM_APP_SECRET=abc123def456...

# Twitter/X API
TWITTER_API_KEY=abc123def456...
TWITTER_API_SECRET=abc123def456ghi789...
```

Then restart your services:
```bash
make down && make up
```

---

## Can I Skip This?

**Yes!** You can run the Creator Dashboard without social media APIs.

### What Works Without APIs:
✅ Video upload and processing
✅ Platform-specific adaptations (YouTube, Instagram, TikTok, Twitter formats)
✅ AI-generated titles, descriptions, hashtags
✅ Thumbnail generation
✅ Full dashboard interface
✅ Content management

### What Requires APIs:
❌ Actually posting to YouTube
❌ Actually posting to Instagram
❌ Actually posting to Twitter/X
❌ Real analytics from platforms
❌ Scheduled publishing to platforms

**Recommendation**: Start without APIs to test the system, then add them when ready to go live.

---

## Cost Breakdown

| Platform | Free Tier | Paid Tier | What You Get |
|----------|-----------|-----------|--------------|
| **YouTube** | ✅ Yes | N/A | 10,000 units/day (enough for ~6 uploads) |
| **Instagram** | ✅ Yes | N/A | 200 API calls/hour |
| **Twitter/X** | ⚠️ Limited | $100/mo | Free = read-only, Paid = posting |

**Total Monthly Cost**: $0-100 depending on Twitter usage

---

## Time Investment

| Task | Time Required |
|------|---------------|
| YouTube setup | 10 minutes |
| Instagram setup | 15 minutes |
| Twitter setup | 10 minutes |
| Testing credentials | 5 minutes |
| **Total** | **40 minutes** |

---

## Priority Order

If you want to add platforms gradually:

1. **Start with YouTube** (easiest, free, most popular)
2. **Add Instagram** (free, good for visual content)
3. **Add Twitter** (requires paid tier for posting)
4. **Skip TikTok** (requires business verification, takes weeks)

---

## Detailed Documentation

For complete step-by-step instructions with screenshots:

📘 **[SOCIAL_MEDIA_API_SETUP.md](SOCIAL_MEDIA_API_SETUP.md)** - Full detailed guide

📋 **[API_CREDENTIALS_QUICK_REFERENCE.md](API_CREDENTIALS_QUICK_REFERENCE.md)** - Quick reference

🚀 **[GET_STARTED.md](GET_STARTED.md)** - Complete getting started guide

---

## Testing Your Setup

After adding credentials, test each platform:

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

Or simply try uploading and distributing content through the dashboard!

---

## Common Questions

**Q: Do I need all three platforms?**
A: No, you can use any combination. Start with one and add more later.

**Q: Can I use my personal accounts?**
A: Yes for YouTube and Twitter. Instagram requires a Business account.

**Q: What if I don't want to pay for Twitter?**
A: You can skip Twitter or use the free tier for testing (read-only).

**Q: How long do credentials last?**
A: YouTube and Instagram tokens can expire. Twitter API keys are permanent until revoked.

**Q: Can I change credentials later?**
A: Yes, just update `.env` and restart: `make down && make up`

**Q: Are credentials secure?**
A: Yes, they're stored in `.env` which is not committed to Git (in `.gitignore`).

---

## Next Steps

1. ✅ Read this summary
2. ✅ Decide which platforms you want
3. ✅ Follow the detailed guide for each platform
4. ✅ Add credentials to `.env`
5. ✅ Restart services
6. ✅ Test by uploading and distributing content

---

## Need Help?

- 📖 Full guide: [SOCIAL_MEDIA_API_SETUP.md](SOCIAL_MEDIA_API_SETUP.md)
- 🐛 Troubleshooting: See "Troubleshooting" section in the full guide
- 📝 Logs: Run `make logs` to see what's happening
- 💬 Support: Open an issue on GitHub

---

**Remember**: You can always start without social media APIs and add them later when you're ready to go live! 🚀
