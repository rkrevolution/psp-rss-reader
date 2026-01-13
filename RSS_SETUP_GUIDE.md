# RSS Feed Setup Guide for Groups.io

This guide shows you how to create and use your own RSS feed from groups.io subscriptions.

## Quick Start

### Option 1: Generate Once (Static Feed)

Generate an RSS feed file that you can open in any RSS reader:

```bash
# Install required Python package
pip3 install requests

# Generate the feed
python3 generate_rss_feed.py
```

This creates `feed.xml` which you can:
- Open directly in an RSS reader
- Upload to a web server
- View locally

### Option 2: Live Server (Auto-Updating Feed)

Run a local web server that automatically refreshes the feed every 30 minutes:

```bash
# Install required package
pip3 install requests

# Start the server
python3 rss_server.py

# Access at: http://localhost:8000/feed.xml
```

The server will:
- ✓ Generate the feed immediately
- ✓ Auto-refresh every 30 minutes
- ✓ Serve the feed at http://localhost:8000/feed.xml
- ✓ Provide manual refresh at http://localhost:8000/refresh

---

## Automated Refresh with Cron

To automatically regenerate the feed periodically (e.g., every 30 minutes):

### macOS / Linux

1. Open crontab:
```bash
crontab -e
```

2. Add this line (refreshes every 30 minutes):
```
*/30 * * * * cd /Users/spark/Desktop/psp1-1 && /usr/bin/python3 generate_rss_feed.py >> /tmp/rss_feed.log 2>&1
```

3. Save and exit

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Repeat every 30 minutes
4. Action: Start Program
   - Program: `python`
   - Arguments: `generate_rss_feed.py`
   - Start in: `C:\path\to\psp1-1`

---

## Serving the Feed Over Network

### Option A: Simple Python HTTP Server

```bash
# Serve the feed on your local network
python3 -m http.server 8000

# Access from any device on your network:
# http://YOUR_COMPUTER_IP:8000/feed.xml
```

### Option B: Use the RSS Server Script

```bash
python3 rss_server.py 8000
```

Access from other devices: `http://YOUR_COMPUTER_IP:8000/feed.xml`

Find your IP:
- macOS: `ifconfig | grep "inet " | grep -v 127.0.0.1`
- Linux: `ip addr show`
- Windows: `ipconfig`

---

## Customization

Edit `generate_rss_feed.py` to customize:

```python
# Change number of topics per group
TOPICS_PER_GROUP = 20  # Default: 10

# Change feed metadata
FEED_TITLE = "My Custom Feed Title"
FEED_DESCRIPTION = "My feed description"

# Filter specific groups
# In the main() function, add:
INCLUDE_GROUPS = ['parkslopeparents', 'parkslopeparents+Classifieds']
# Then filter: groups = [g for g in groups if g['group_name'] in INCLUDE_GROUPS]
```

---

## RSS Feed Format

The generated feed follows RSS 2.0 standard and includes:

- **Title**: `[GroupName] Topic Subject`
- **Link**: Direct link to the topic on groups.io
- **Description**: Topic summary, author, message count, attachments
- **Date**: Topic creation/update time
- **Category**: Group name
- **GUID**: Unique identifier (topic URL)

Example RSS item:
```xml
<item>
  <title>[parkslopeparents] ISO Babysitter recommendations</title>
  <link>https://groups.parkslopeparents.com/g/Advice/topic/12345</link>
  <description>Looking for babysitter recommendations in Park Slope...
  Posted by: Jane Doe
  Messages: 5</description>
  <pubDate>Mon, 13 Jan 2026 10:30:00 -0800</pubDate>
  <category>parkslopeparents</category>
</item>
```

---

## Troubleshooting

### "No module named 'requests'"

Install the requests library:
```bash
pip3 install requests
```

### "Permission denied"

Make scripts executable:
```bash
chmod +x generate_rss_feed.py
chmod +x rss_server.py
```

### Feed not updating

- Check that cron job is running: `crontab -l`
- Check logs: `tail -f /tmp/rss_feed.log`
- Manually run: `python3 generate_rss_feed.py`

### Port already in use

Use a different port:
```bash
python3 rss_server.py 8080
```

### Empty feed

- Verify API key is correct in `generate_rss_feed.py`
- Check you have `archives_visible` permission for groups
- Run manually to see error messages

---

## Advanced: Deploy to a Server

### Deploy to Always-On Server

If you have a server (Raspberry Pi, VPS, etc.), you can:

1. Copy scripts to server
2. Set up systemd service (Linux):

```bash
# Create service file: /etc/systemd/system/rss-feed.service
[Unit]
Description=Groups.io RSS Feed Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/psp1-1
ExecStart=/usr/bin/python3 /path/to/psp1-1/rss_server.py 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start:
```bash
sudo systemctl enable rss-feed
sudo systemctl start rss-feed
```

### Use ngrok for External Access

Expose your local feed to the internet temporarily:

```bash
# Start the server
python3 rss_server.py 8000

# In another terminal, install and run ngrok
brew install ngrok  # macOS
ngrok http 8000

# ngrok will give you a public URL like:
# https://abc123.ngrok.io/feed.xml
```

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **API Key Protection**: Your API key is hardcoded in the script
   - Don't commit to Git
   - Use environment variable instead:
   ```python
   import os
   API_KEY = os.environ.get('GROUPS_IO_API_KEY')
   ```

2. **Local Network Only**: The server binds to all interfaces (0.0.0.0)
   - Only expose on trusted networks
   - Use firewall rules to restrict access

3. **HTTPS**: The feed server uses HTTP, not HTTPS
   - For public deployment, use reverse proxy (nginx) with SSL
   - Or use a service like Cloudflare Tunnel

---

## Next Steps

- Try the feed in different RSS readers (see mobile app recommendations)
- Set up automated refresh
- Customize which groups/topics to include
- Deploy to a server for 24/7 access
- Create multiple feeds for different group categories
