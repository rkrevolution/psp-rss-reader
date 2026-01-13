# Park Slope Parents RSS Reader

A beautiful, self-hosted RSS feed aggregator for groups.io communities. Combines multiple groups into a unified feed with full message content, search, and filtering.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

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

1. Get your groups.io API key from: https://groups.io/account
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   GROUPS_IO_API_KEY=your_64_character_api_key_here
   ```

### 4. Run the Server

```bash
python3 fastapi_rss_server.py
```

The server will start at:
- 🌐 **Web Reader**: http://localhost:8000/reader
- 📡 **RSS Feed**: http://localhost:8000/feed.xml
- 📚 **API Docs**: http://localhost:8000/docs

## 📱 Mobile Setup

### iPhone/iPad (NetNewsWire)

1. Install **NetNewsWire** (free from App Store)
2. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
3. In NetNewsWire: **Add Feed** → `http://YOUR_IP:8000/feed.xml`
4. Enjoy your unified feed!

### Android (Feeder)

1. Install **Feeder** (free from F-Droid or Play Store)
2. Open Feeder → **+** button
3. Add feed: `http://YOUR_IP:8000/feed.xml`

### Remote Access (ngrok)

For access from anywhere:

```bash
# Terminal 1: Start the RSS server
python3 fastapi_rss_server.py

# Terminal 2: Start ngrok
ngrok http 8000
```

Use the HTTPS URL ngrok provides in your RSS reader!

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

### Deploy to Cloud (24/7 Access)

#### Railway.app (Free Tier)

1. Push this repo to GitHub
2. Connect to Railway: https://railway.app
3. Deploy from GitHub repo
4. Add environment variable: `GROUPS_IO_API_KEY`
5. Get permanent URL!

#### Render.com (Free Tier)

1. Push to GitHub
2. Create new Web Service on Render
3. Build command: `pip install -r requirements.txt`
4. Start command: `python3 fastapi_rss_server.py`
5. Add environment variable
6. Deploy!

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
