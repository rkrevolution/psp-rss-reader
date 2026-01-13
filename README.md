# Park Slope Parents RSS Reader

A beautiful, self-hosted RSS feed aggregator for groups.io communities. Combines multiple groups into a unified feed with full message content, search, and filtering.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> ⚠️ **Important:** This project requires your own groups.io API key. Never share your API key or commit it to version control.

## ✨ Features

- 📡 **Unified RSS Feed** - Combines topics from all your subscribed groups
- 📖 **Full Content** - Includes complete message text (no authentication needed to read!)
- 🎨 **Beautiful Web Reader** - Modern, responsive interface with search and filters
- 🔄 **Auto-Refresh** - Updates every 30 minutes automatically
- 📱 **Mobile-Friendly** - Works with any RSS reader (NetNewsWire, Feeder, etc.)
- 🔒 **Privacy-First** - Self-hosted, your data stays with you
- ⚡ **Fast** - Built with FastAPI for high performance

## 📸 Screenshots

**Web Reader:**
- Clean card-based layout
- Filter by group (Advice, Classifieds, May2026, etc.)
- Search across all topics
- Collapsible full message content
- Color-coded group badges

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/psp-rss-reader.git
cd psp-rss-reader
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

⚠️ **IMPORTANT: You must use your own groups.io API key**

1. **Get your API key:**
   - Go to https://groups.io/account
   - Scroll to "API Keys" section
   - Click "Create New API Key"
   - Copy the 64-character key (you won't be able to see it again!)

2. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

3. **Add your API key to .env:**
   ```bash
   # Edit .env and replace with YOUR actual API key
   GROUPS_IO_API_KEY=paste_your_64_character_api_key_here
   ```

   **Note:** Never share your API key or commit the `.env` file to git!

### 4. Run the Server

```bash
python3 fastapi_rss_server.py
```

The server will start at:
- 🌐 **Web Reader**: http://localhost:8000/reader
- 📡 **RSS Feed**: http://localhost:8000/feed.xml
- 📚 **API Docs**: http://localhost:8000/docs

> ⚠️ **Important:** `localhost` only works on your computer. For mobile access or 24/7 availability, see [Free Cloud Deployment](#-free-cloud-deployment) below!

## 🌐 Free Cloud Deployment

**Want to access from anywhere? Deploy for FREE in 5 minutes!**

Running locally means:
- ❌ Only works on your WiFi network
- ❌ Stops when computer turns off
- ❌ Can't use on mobile (unless on same network)

**Free cloud options give you:**
- ✅ Permanent HTTPS URL (e.g., `https://your-app.onrender.com/feed.xml`)
- ✅ Works from anywhere (cellular, any WiFi)
- ✅ 24/7 availability
- ✅ No computer needed

**Easiest free option - Render.com (5 minutes):**

1. Push this repo to GitHub
2. Go to https://render.com (sign up free)
3. Create "New Web Service" → Connect your repo
4. Add environment variable: `GROUPS_IO_API_KEY`
5. Deploy!
6. Get permanent URL: `https://psp-rss-reader.onrender.com/feed.xml`

**Other free options:** Railway.app, Fly.io, ngrok

📚 **[Full deployment guide with all free options →](DEPLOYMENT.md)**

## 📱 Mobile Setup

### Best Way: Use Cloud Deployment

**After deploying to Render/Railway** (see above), simply use your cloud URL:

**iPhone/iPad (NetNewsWire):**
1. Install NetNewsWire (free from App Store)
2. Add Feed → `https://psp-rss-reader.onrender.com/feed.xml`
3. Done! Works everywhere (WiFi, cellular)

**Android (Feeder):**
1. Install Feeder (free from F-Droid or Play Store)
2. Add Feed → `https://psp-rss-reader.onrender.com/feed.xml`
3. Done!

### Alternative: Local Network Only

**If running locally** (only works on same WiFi):

1. Find your computer's IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   # Example output: 192.168.1.100
   ```

2. Use: `http://YOUR_IP:8000/feed.xml`
   - ⚠️ Only works on same WiFi
   - ⚠️ Stops working when computer sleeps
   - ⚠️ IP address can change

**Recommendation:** Deploy to cloud instead for reliable access!

## ⚙️ Configuration

Edit `.env` to customize:

```bash
# API Key (required)
GROUPS_IO_API_KEY=your_api_key_here

# Number of topics to fetch per group (default: 10)
TOPICS_PER_GROUP=15

# Auto-refresh interval in minutes (default: 30)
REFRESH_INTERVAL_MINUTES=15
```

## 🎯 What Makes This Special?

### Full Message Content

Unlike typical RSS feeds that only show previews, this fetches the **complete first message** of each topic. This means:

- ✅ Read everything directly in your RSS reader
- ✅ No authentication required
- ✅ Works offline once cached
- ✅ Collapsible for clean viewing

### Smart Preview System

Each topic shows:
1. **Metadata**: Author, reply count, attachments
2. **Preview**: First 200 characters
3. **▶ Read full message**: Collapsible section with complete formatted content

### Multi-Group Aggregation

Automatically combines topics from:
- Main community group (Advice)
- Specialty groups (Classifieds, birth month groups, etc.)
- All sorted by most recent

## 🛠️ Advanced Usage

### Run as Background Service (Linux)

Create systemd service:

```bash
sudo nano /etc/systemd/system/psp-rss.service
```

```ini
[Unit]
Description=PSP RSS Feed Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/psp-rss-reader
EnvironmentFile=/path/to/psp-rss-reader/.env
ExecStart=/usr/bin/python3 fastapi_rss_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable psp-rss
sudo systemctl start psp-rss
```

### Customize Feed Appearance

Edit `feed_reader.html` to change:
- Colors and styling
- Filter buttons
- Card layout
- Typography

## 📁 Project Structure

```
psp-rss-reader/
├── fastapi_rss_server.py      # Main FastAPI server
├── feed_reader.html            # Web-based feed reader UI
├── generate_rss_feed.py        # Standalone RSS generator
├── rss_server.py               # Alternative simple server
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## 🔒 Security Notes

⚠️ **Important:**

- Your API key is stored in `.env` (never committed to git)
- The `.gitignore` file prevents accidental commits
- For public deployments, use environment variables
- The server binds to `0.0.0.0` - use firewall rules for production

## 🤝 Contributing

Contributions welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

## 📝 License

MIT License - feel free to use this for your own communities!

## 🙏 Acknowledgments

- Built for the **Park Slope Parents** community
- Powered by the **groups.io API**
- Uses **FastAPI** for the backend
- Inspired by the need for better RSS feeds with full content

## 📞 Support

Issues? Questions?

- Open an issue on GitHub
- Check the [groups.io API docs](https://groups.io/api)
- Review the [FastAPI documentation](https://fastapi.tiangolo.com/)

## 🚀 What's Next?

Planned features:
- [ ] Email notifications for specific keywords
- [ ] Multiple feed configurations
- [ ] Reply functionality
- [ ] Advanced filtering rules
- [ ] Mobile app (maybe!)

---

**Made with ❤️ for parents who need a better way to stay connected**
