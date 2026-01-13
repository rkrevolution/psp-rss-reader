# Free Deployment Options

This guide shows you how to deploy your RSS reader to the cloud for **free** so it's accessible from anywhere, not just your local network.

## 🌐 Why Deploy to the Cloud?

**Local (localhost) limitations:**
- ❌ Only works on your computer
- ❌ Only accessible on your WiFi network
- ❌ Stops working when computer is off
- ❌ Requires computer IP address (which can change)

**Cloud deployment benefits:**
- ✅ **Always available** (24/7)
- ✅ **Accessible from anywhere** (cellular data, any WiFi)
- ✅ **Permanent URL** (no IP address needed)
- ✅ **HTTPS** (secure, works with all RSS readers)
- ✅ **Auto-restarts** if it crashes

---

## 🆓 Best Free Options (Ranked)

### 1. Render.com ⭐ EASIEST

**Free Tier:**
- 750 hours/month free
- Spins down after 15 minutes of inactivity
- Takes 30-60 seconds to wake up on first request
- Perfect for RSS feeds (they don't need instant response)

**Setup (5 minutes):**

1. **Push to GitHub** (if not already):
   ```bash
   git push
   ```

2. **Go to Render:**
   - Visit: https://render.com
   - Sign up with GitHub

3. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your `psp-rss-reader` repo
   - Render will auto-detect settings from `render.yaml`

4. **Add Environment Variable:**
   - In Render dashboard → Environment
   - Add: `GROUPS_IO_API_KEY` = `your_api_key_here`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Get your URL: `https://psp-rss-reader.onrender.com`

6. **Add to RSS Reader:**
   - Use: `https://psp-rss-reader.onrender.com/feed.xml`
   - Done! ✅

**Pros:**
- ✅ Easiest setup
- ✅ Auto-deploys on git push
- ✅ Free HTTPS
- ✅ Built-in monitoring

**Cons:**
- ⚠️ Spins down after inactivity (first request slower)

---

### 2. Railway.app ⭐ BEST PERFORMANCE

**Free Tier:**
- $5 credit/month
- ~500 hours of runtime
- Stays awake (no spin-down)
- Fast deployment

**Setup (5 minutes):**

1. **Go to Railway:**
   - Visit: https://railway.app
   - Sign up with GitHub

2. **Deploy from GitHub:**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `psp-rss-reader`
   - Railway auto-detects settings from `railway.toml`

3. **Add Environment Variable:**
   - Click on service → "Variables"
   - Add: `GROUPS_IO_API_KEY` = `your_api_key_here`

4. **Generate Domain:**
   - Settings → "Generate Domain"
   - Get URL: `https://psp-rss-reader.up.railway.app`

5. **Add to RSS Reader:**
   - Use: `https://psp-rss-reader.up.railway.app/feed.xml`

**Pros:**
- ✅ No spin-down (always fast)
- ✅ Excellent performance
- ✅ Simple deployment
- ✅ Great free tier

**Cons:**
- ⚠️ Limited to ~500 hours/month on free tier

---

### 3. Fly.io

**Free Tier:**
- 3 shared VMs
- 160GB bandwidth
- No spin-down

**Setup (10 minutes):**

1. **Install flyctl:**
   ```bash
   # macOS
   brew install flyctl

   # Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   flyctl auth login
   ```

3. **Launch app:**
   ```bash
   flyctl launch
   # Answer prompts:
   # - App name: psp-rss-reader
   # - Region: choose closest to you
   # - Deploy now: No
   ```

4. **Set environment variable:**
   ```bash
   flyctl secrets set GROUPS_IO_API_KEY=your_api_key_here
   ```

5. **Deploy:**
   ```bash
   flyctl deploy
   ```

6. **Get URL:**
   ```bash
   flyctl info
   # Use: https://psp-rss-reader.fly.dev/feed.xml
   ```

**Pros:**
- ✅ No spin-down
- ✅ Good performance
- ✅ More control

**Cons:**
- ⚠️ Requires CLI installation
- ⚠️ Slightly more complex

---

### 4. ngrok (Temporary/Testing)

**Free Tier:**
- Unlimited usage
- URL changes on restart
- Good for testing

**Setup (2 minutes):**

1. **Install ngrok:**
   ```bash
   # macOS
   brew install ngrok

   # Or download from: https://ngrok.com/download
   ```

2. **Start your local server:**
   ```bash
   python3 fastapi_rss_server.py
   ```

3. **In another terminal, start ngrok:**
   ```bash
   ngrok http 8000
   ```

4. **Copy the HTTPS URL:**
   ```
   Forwarding  https://abc123.ngrok.io -> http://localhost:8000
   ```

5. **Use in RSS reader:**
   ```
   https://abc123.ngrok.io/feed.xml
   ```

**Pros:**
- ✅ Instant setup
- ✅ No code changes needed
- ✅ Free HTTPS

**Cons:**
- ❌ URL changes every restart
- ❌ Requires computer to stay on
- ❌ Not truly "cloud" (just tunnels to your computer)

---

## 📊 Comparison Table

| Platform | Free Hours | Spin Down? | Complexity | Best For |
|----------|-----------|------------|------------|----------|
| **Render** | 750/month | Yes (15min) | ⭐ Easy | Most users |
| **Railway** | ~500/month | No | ⭐⭐ Easy | Performance |
| **Fly.io** | Unlimited* | No | ⭐⭐⭐ Medium | Advanced |
| **ngrok** | Unlimited | N/A | ⭐ Easy | Testing |

*Within free tier limits

---

## 🎯 Recommended Setup

**For most people:**
1. Start with **Render.com** (easiest)
2. If you need no-spin-down, use **Railway.app**
3. For testing, use **ngrok**

**My pick:** Render.com for simplicity + Railway.app if you need it always fast.

---

## ⚙️ Post-Deployment Setup

Once deployed, your feed will be at:
```
https://your-app-name.platform.com/feed.xml
```

**Add to mobile RSS readers:**

**iPhone (NetNewsWire):**
1. Open NetNewsWire
2. Add Feed → `https://your-app.onrender.com/feed.xml`
3. Syncs via iCloud!

**Android (Feeder):**
1. Open Feeder
2. + → Add Feed → `https://your-app.onrender.com/feed.xml`

---

## 🔧 Troubleshooting

### "Application Error" on Render

**Fix:** Check environment variables
- Make sure `GROUPS_IO_API_KEY` is set in Render dashboard
- Check logs: Render Dashboard → Logs

### Railway deploys but crashes

**Fix:** Check your API key
```bash
railway logs
# Look for "GROUPS_IO_API_KEY not found"
```

### Slow first load on Render

**Normal!** Free tier spins down after 15 minutes of inactivity.
- First request wakes it up (~30-60 seconds)
- Subsequent requests are fast
- Consider Railway if this bothers you

### Feed not updating

**Check auto-refresh:**
- Visit: `https://your-app.com/status`
- Should show `"refresh_interval_minutes": 30`

---

## 💰 Cost Comparison

All options listed are **100% FREE** for this use case!

**Why?**
- RSS feeds use minimal resources
- Low traffic (you're the only user)
- Small data transfer
- All platforms have generous free tiers

---

## 🚀 Next Steps

After deploying:

1. **Test your feed:**
   ```bash
   curl https://your-app.onrender.com/status
   ```

2. **Add to RSS reader** (mobile/desktop)

3. **Share with friends** (optional - they need their own deployment)

4. **Set it and forget it** - it will auto-update every 30 minutes!

---

## 📝 Notes

- You can deploy to multiple platforms (try them all!)
- Each deployment is independent
- Free tiers are perfect for personal RSS feeds
- All provide HTTPS automatically (secure)

**Questions?** Open an issue on GitHub!
