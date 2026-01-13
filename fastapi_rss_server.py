#!/usr/bin/env python3
"""
Groups.io RSS Feed Server (FastAPI)

A production-ready RSS feed server using FastAPI.
Mobile-friendly with automatic HTTPS support via ngrok/Cloudflare Tunnel.

Usage:
    # Install dependencies first
    pip install fastapi uvicorn requests python-dotenv

    # Run the server
    python3 fastapi_rss_server.py

Access:
    http://localhost:8000/feed.xml
    http://localhost:8000/docs (API documentation)
"""

from fastapi import FastAPI, Response, BackgroundTasks
from fastapi.responses import HTMLResponse
import requests
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import time
from contextlib import asynccontextmanager
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("GROUPS_IO_API_KEY")
if not API_KEY:
    raise ValueError("GROUPS_IO_API_KEY not found in environment variables. Please create a .env file.")

BASE_URL = "https://groups.io/api/v1"
TOPICS_PER_GROUP = int(os.getenv("TOPICS_PER_GROUP", "10"))
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL_MINUTES", "30")) * 60  # Convert to seconds

# Feed metadata
FEED_TITLE = "Park Slope Parents - All Groups"
FEED_LINK = "https://groups.parkslopeparents.com"
FEED_DESCRIPTION = "Recent topics from all my Park Slope Parents groups"

# Cache
feed_cache = {"xml": None, "last_updated": None}
group_alias_cache = {}  # Maps group_id to URL alias


def make_api_request(endpoint, params=None):
    """Make an authenticated API request to groups.io"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None


def get_subscriptions():
    """Get all groups the user is subscribed to"""
    data = make_api_request("getsubs")
    groups = data.get("data", []) if data else []

    # Cache group aliases for correct URL generation
    for group in groups:
        group_id = group['group_id']
        if group_id not in group_alias_cache:
            group_info = make_api_request("getgroup", {"group_id": group_id})
            if group_info and 'group_url' in group_info:
                # Extract alias from URL (e.g., .../g/Advice -> Advice)
                url_parts = group_info['group_url'].split('/g/')
                if len(url_parts) > 1:
                    group_alias_cache[group_id] = url_parts[1]

    return groups


def get_topics(group_id, group_name, limit=10):
    """Get recent topics from a specific group"""
    params = {"group_id": group_id, "limit": limit}
    data = make_api_request("gettopics", params)
    return data.get("data", []) if data else []


def get_topic_full_content(topic_id):
    """Get the full content of the first message in a topic"""
    params = {"topic_id": topic_id}
    data = make_api_request("gettopic", params)

    if data and "data" in data and len(data["data"]) > 0:
        first_message = data["data"][0]
        return first_message.get("body", "")
    return None


def html_to_text(html_string):
    """Basic HTML tag removal"""
    import re
    text = re.sub(r'<[^>]+>', '', html_string or '')
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'")
    return text.strip()


def parse_iso_date(date_string):
    """Parse ISO 8601 date string"""
    try:
        if date_string:
            if '.' in date_string:
                date_string = date_string.split('.')[0] + date_string.split('.')[-1][-6:]
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except:
        pass
    return datetime.now()


def create_rss_feed(all_topics):
    """Generate RSS 2.0 XML from topics"""
    rss = Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

    channel = SubElement(rss, 'channel')

    # Channel metadata
    SubElement(channel, 'title').text = FEED_TITLE
    SubElement(channel, 'link').text = FEED_LINK
    SubElement(channel, 'description').text = FEED_DESCRIPTION
    SubElement(channel, 'language').text = 'en-us'
    SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

    # Add self-reference
    atom_link = SubElement(channel, '{http://www.w3.org/2005/Atom}link')
    atom_link.set('href', f'{FEED_LINK}/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')

    # Add items
    for topic in all_topics:
        item = SubElement(channel, 'item')

        SubElement(item, 'title').text = f"[{topic['group_name']}] {topic['subject']}"

        # Get the correct URL alias from cache
        group_id = topic.get('group_id_for_url')
        group_alias = group_alias_cache.get(group_id, topic['group_name'].split('+')[-1])
        topic_url = f"https://groups.parkslopeparents.com/g/{group_alias}/topic/{topic['id']}"
        SubElement(item, 'link').text = topic_url

        # Get full message content
        full_content = topic.get('full_body')

        if full_content:
            # Clean preview from summary
            summary = html_to_text(topic.get('summary', ''))
            if len(summary) > 200:
                summary = summary[:200] + "..."

            # Metadata header
            meta = f"<p><em>Posted by {topic.get('name', 'Unknown')}"
            if topic.get('num_messages', 0) > 1:
                meta += f" • {topic.get('num_messages', 0)} replies"
            if topic.get('has_attachments'):
                meta += " • 📎 Attachments"
            meta += "</em></p>"

            # Build description with preview and collapsible full content
            desc = meta
            desc += f"<p><strong>Preview:</strong> {summary}</p>"
            desc += f"<details><summary><strong>▶ Read full message</strong></summary><hr>{full_content}</details>"
        else:
            # Fallback to summary if full content not available
            summary = html_to_text(topic.get('summary', ''))
            if len(summary) > 500:
                summary = summary[:500] + "..."
            desc = f"{summary}\n\nPosted by: {topic.get('name', 'Unknown')}\nMessages: {topic.get('num_messages', 0)}"
            if topic.get('has_attachments'):
                desc += "\nHas attachments"

        SubElement(item, 'description').text = desc

        pub_date = parse_iso_date(topic.get('updated') or topic.get('created'))
        SubElement(item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y %H:%M:%S %z')

        guid = SubElement(item, 'guid')
        guid.set('isPermaLink', 'true')
        guid.text = topic_url

        SubElement(item, 'author').text = topic.get('name', 'Unknown')
        SubElement(item, 'category').text = topic['group_name']

    # Pretty print
    xml_string = minidom.parseString(tostring(rss)).toprettyxml(indent="  ")
    return xml_string


def generate_feed():
    """Generate the RSS feed and cache it"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Generating RSS feed...")

    groups = get_subscriptions()
    if not groups:
        print("No groups found")
        return None

    all_topics = []
    for group in groups:
        if not group.get('perms', {}).get('archives_visible', False):
            continue

        group_id = group['group_id']
        group_name = group['group_name']

        topics = get_topics(group_id, group_name, TOPICS_PER_GROUP)

        for topic in topics:
            topic['group_name'] = group_name
            topic['group_id_for_url'] = group_id  # Store for URL generation
            topic['nice_group_name'] = group.get('nice_group_name', group_name)

        all_topics.extend(topics)
        print(f"  ✓ {group_name}: {len(topics)} topics")

    # Fetch full content for each topic
    print(f"\n  Fetching full content for {len(all_topics)} topics...")
    for i, topic in enumerate(all_topics, 1):
        full_body = get_topic_full_content(topic['id'])
        if full_body:
            topic['full_body'] = full_body
            print(f"    ✓ {i}/{len(all_topics)}: {topic['subject'][:50]}...")
        else:
            print(f"    ✗ {i}/{len(all_topics)}: Failed to fetch content")

    # Sort by most recent
    all_topics.sort(key=lambda x: x.get('updated') or x.get('created'), reverse=True)

    # Generate XML
    xml = create_rss_feed(all_topics)

    # Cache it
    feed_cache['xml'] = xml
    feed_cache['last_updated'] = datetime.now()

    print(f"  ✓ Feed generated with {len(all_topics)} total topics")
    return xml


async def refresh_feed_periodically():
    """Background task to refresh feed every 30 minutes"""
    while True:
        await asyncio.sleep(REFRESH_INTERVAL)
        generate_feed()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Generate initial feed
    print("=" * 60)
    print("Groups.io RSS Feed Server (FastAPI)")
    print("=" * 60)
    generate_feed()

    # Start background refresh task
    task = asyncio.create_task(refresh_feed_periodically())
    print(f"\n✓ Auto-refresh enabled (every {REFRESH_INTERVAL // 60} minutes)")

    yield

    # Shutdown
    task.cancel()


# Create FastAPI app
app = FastAPI(
    title="Groups.io RSS Feed",
    description="RSS feed generator for groups.io subscriptions",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Homepage with instructions"""
    last_update = feed_cache['last_updated']
    last_update_str = last_update.strftime('%Y-%m-%d %H:%M:%S') if last_update else "Never"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Groups.io RSS Feed</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                line-height: 1.6;
            }}
            .feed-url {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 8px;
                font-family: monospace;
                word-break: break-all;
                margin: 20px 0;
            }}
            .button {{
                display: inline-block;
                background: #007bff;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                margin: 5px;
            }}
            .status {{
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 12px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            h1 {{ color: #333; }}
            code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <h1>📡 Groups.io RSS Feed</h1>

        <div class="status">
            ✓ Server is running<br>
            Last updated: {last_update_str}
        </div>

        <h2>Your RSS Feed URL</h2>
        <div class="feed-url">
            <a href="/feed.xml" id="feed-url">Click to view feed</a>
        </div>

        <h2>Quick Actions</h2>
        <a href="/feed.xml" class="button">📄 View Feed</a>
        <a href="/refresh" class="button">🔄 Refresh Now</a>
        <a href="/docs" class="button">📚 API Docs</a>

        <h2>Mobile Setup</h2>
        <p><strong>For iPhone/iPad (NetNewsWire):</strong></p>
        <ol>
            <li>Install NetNewsWire from the App Store (free)</li>
            <li>Copy this URL: <code id="mobile-url"></code></li>
            <li>Open NetNewsWire → Add Feed → Paste URL</li>
        </ol>

        <p><strong>For Android (Feeder):</strong></p>
        <ol>
            <li>Install Feeder from F-Droid or Play Store (free)</li>
            <li>Open Feeder → + → Add Feed</li>
            <li>Paste the URL above</li>
        </ol>

        <h2>Endpoints</h2>
        <ul>
            <li><code>/feed.xml</code> - RSS feed</li>
            <li><code>/refresh</code> - Force refresh the feed</li>
            <li><code>/status</code> - Server status</li>
            <li><code>/docs</code> - API documentation</li>
        </ul>

        <script>
            // Auto-fill URLs with current host
            const currentUrl = window.location.href;
            const feedUrl = currentUrl.replace(/\/$/, '') + '/feed.xml';
            document.getElementById('feed-url').href = feedUrl;
            document.getElementById('feed-url').textContent = feedUrl;
            document.getElementById('mobile-url').textContent = feedUrl;
        </script>
    </body>
    </html>
    """
    return html


@app.get("/feed.xml")
async def get_feed():
    """Get the RSS feed"""
    xml = feed_cache.get('xml')

    if not xml:
        # Generate if not cached
        xml = generate_feed()

    return Response(content=xml, media_type="application/rss+xml")


@app.get("/refresh")
async def refresh_feed(background_tasks: BackgroundTasks):
    """Manually refresh the feed"""
    background_tasks.add_task(generate_feed)
    return {
        "status": "refreshing",
        "message": "Feed refresh started in background"
    }


@app.get("/status")
async def get_status():
    """Get server status"""
    last_update = feed_cache.get('last_updated')

    return {
        "status": "running",
        "last_updated": last_update.isoformat() if last_update else None,
        "feed_cached": feed_cache.get('xml') is not None,
        "refresh_interval_minutes": REFRESH_INTERVAL // 60
    }


@app.get("/reader", response_class=HTMLResponse)
async def feed_reader():
    """Web-based feed reader"""
    with open('feed_reader.html', 'r') as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("Starting FastAPI RSS Feed Server")
    print("=" * 60)
    print("\nAccess points:")
    print("  • Homepage:  http://localhost:8000")
    print("  • RSS Feed:  http://localhost:8000/feed.xml")
    print("  • API Docs:  http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
