# Quick Start: RSS Feed for Mobile

The **easiest way** to get your groups.io RSS feed on your phone.

---

## 🚀 Super Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd /Users/spark/Desktop/psp1-1

# Option A: Using pip (if allowed)
pip3 install fastapi uvicorn requests

# Option B: Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
python3 fastapi_rss_server.py
```

You'll see:
```
Starting FastAPI RSS Feed Server
Access points:
  • Homepage:  http://localhost:8000
  • RSS Feed:  http://localhost:8000/feed.xml
```

### Step 3: Access on Mobile

**Two options:**

#### Option A: Same WiFi Network (Easiest)
1. Find your computer's IP address:
   ```bash
   # On Mac
   ifconfig | grep "inet " | grep -v 127.0.0.1
   # Look for something like: 192.168.1.100
   ```

2. On your phone, use:
   ```
   http://YOUR_IP:8000/feed.xml
   ```
   Example: `http://192.168.1.100:8000/feed.xml`

#### Option B: ngrok (Access from anywhere)
1. Install ngrok: https://ngrok.com/download
2. Run:
   ```bash
   ngrok http 8000
   ```
3. Use the HTTPS URL ngrok gives you:
   ```
   https://abc123.ngrok.io/feed.xml
   ```

---

## 📱 Mobile App Setup

### iPhone/iPad (NetNewsWire - Free)

1. **Install NetNewsWire**
   - App Store → Search "NetNewsWire" → Install (100% free)

2. **Add Your Feed**
   - Open NetNewsWire
   - Tap "+" in top right
   - Paste your feed URL: `http://YOUR_IP:8000/feed.xml`
   - Tap "Add"

3. **Done!** Topics will appear in NetNewsWire

**Bonus:** Install on Mac too → Syncs via iCloud automatically!

---

### Android (Feeder - Free)

1. **Install Feeder**
   - F-Droid: https://f-droid.org/packages/com.nononsenseapps.feeder/
   - Or Google Play Store → Search "Feeder"

2. **Add Your Feed**
   - Open Feeder
   - Tap "+" button
   - Enter feed URL: `http://YOUR_IP:8000/feed.xml`
   - Tap "Add"

3. **Done!** Topics will appear in Feeder

---

## 🌐 Best Option: Access from Anywhere

### Using ngrok (Easiest for mobile)

**Why:** Access your feed from anywhere, not just home WiFi

**Setup:**

```bash
# Terminal 1: Start your RSS server
python3 fastapi_rss_server.py

# Terminal 2: Start ngrok
ngrok http 8000
```

ngrok will show:
```
Forwarding   https://abc-123-def.ngrok.io -> http://localhost:8000
```

**Use the HTTPS URL in your mobile RSS reader!**
- More secure (HTTPS)
- Works on cellular data
- Works anywhere in the world
- Free tier available

---

## 🎯 Complete Mobile Workflow

**The best setup:**

```bash
# 1. Start server (keeps running)
python3 fastapi_rss_server.py

# 2. In another terminal, start ngrok
ngrok http 8000

# 3. On your phone:
# - Install NetNewsWire (iOS) or Feeder (Android)
# - Add feed: https://YOUR-NGROK-URL.ngrok.io/feed.xml
# - Enjoy!
```

**The feed auto-refreshes every 30 minutes** ✓

---

## 🔧 Alternative: Deploy to Cloud (Always Available)

If you want 24/7 access without running your computer:

### Option 1: Railway.app (Free tier)

1. Create `railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python3 fastapi_rss_server.py"
```

2. Push to GitHub
3. Deploy on Railway: https://railway.app
4. Get permanent URL!

### Option 2: Render.com (Free tier)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `python3 fastapi_rss_server.py`
6. Get permanent URL!

### Option 3: Fly.io (Free tier)

```bash
# Install flyctl
brew install flyctl

# Login and deploy
flyctl auth login
flyctl launch
flyctl deploy
```

---

## 📊 Feature Comparison

| Method | Setup Time | Cost | Mobile Access | 24/7 Available |
|--------|-----------|------|---------------|----------------|
| **Local WiFi** | 2 min | Free | WiFi only | While computer on |
| **ngrok** | 5 min | Free | Anywhere | While computer on |
| **Railway/Render** | 10 min | Free | Anywhere | Always |

---

## 🎨 Using the Web Interface

Open `http://localhost:8000` in a browser to see:

- ✓ Homepage with instructions
- ✓ Current feed status
- ✓ One-click feed refresh
- ✓ API documentation at `/docs`
- ✓ Mobile-friendly design

---

## 🔄 Auto-Refresh Setup

The FastAPI server **automatically refreshes** every 30 minutes.

To change refresh interval, edit `fastapi_rss_server.py`:

```python
REFRESH_INTERVAL = 1800  # Change to desired seconds
# 900 = 15 minutes
# 1800 = 30 minutes (default)
# 3600 = 1 hour
```

---

## ⚡ Quick Troubleshooting

**"Connection refused" on mobile:**
- Make sure phone and computer are on same WiFi
- Check firewall isn't blocking port 8000
- Verify IP address is correct

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**Want to run in background:**
```bash
# macOS/Linux
nohup python3 fastapi_rss_server.py > rss.log 2>&1 &

# Or use screen/tmux
screen -S rss
python3 fastapi_rss_server.py
# Ctrl+A then D to detach
```

---

## 📱 Recommended Mobile Apps

### iOS
- **NetNewsWire** (Best, 100% free, open source)
- Reeder 5 (Paid, beautiful)
- lire (Paid, minimal)

### Android
- **Feeder** (Best, free, open source)
- Read You (Free, Material You design)
- Readrops (Free, works with FreshRSS)

### Cross-Platform Web
- **Miniflux** (Self-hosted)
- **FreshRSS** (Self-hosted, syncs to mobile apps)

---

## 🎉 You're Done!

Your groups.io topics are now available as an RSS feed on your phone!

**Next steps:**
- Try different RSS readers to find your favorite
- Deploy to cloud for 24/7 access
- Customize the feed (edit `TOPICS_PER_GROUP` in the script)
- Share with other PSP members!
