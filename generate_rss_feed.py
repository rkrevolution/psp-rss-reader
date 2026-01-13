#!/usr/bin/env python3
"""
Groups.io to RSS Feed Generator

This script fetches recent topics from your groups.io subscriptions
and generates a standard RSS 2.0 feed that you can use with any RSS reader.

Usage:
    python3 generate_rss_feed.py

The script will:
1. Fetch all your subscribed groups
2. Get recent topics from each group
3. Generate an RSS feed (feed.xml)
4. Optionally serve it via a simple web server
"""

import requests
import json
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import sys

# Configuration
API_KEY = "521cb1f0b6ef044036181a906e8af6e66bb122a0beefdec72963f7d2f972c467"
BASE_URL = "https://groups.io/api/v1"
OUTPUT_FILE = "feed.xml"

# RSS Feed Settings
FEED_TITLE = "Park Slope Parents - All Groups"
FEED_LINK = "https://groups.parkslopeparents.com"
FEED_DESCRIPTION = "Recent topics from all my Park Slope Parents groups"
TOPICS_PER_GROUP = 10  # How many recent topics to fetch per group


def make_api_request(endpoint, params=None):
    """Make an authenticated API request to groups.io"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request to {endpoint}: {e}")
        return None


def get_subscriptions():
    """Get all groups the user is subscribed to"""
    print("Fetching your group subscriptions...")
    data = make_api_request("getsubs")

    if data and "data" in data:
        groups = data["data"]
        print(f"Found {len(groups)} subscribed groups")
        return groups
    return []


def get_topics(group_id, group_name, limit=10):
    """Get recent topics from a specific group"""
    print(f"  Fetching {limit} topics from {group_name}...")

    params = {
        "group_id": group_id,
        "limit": limit
    }

    data = make_api_request("gettopics", params)

    if data and "data" in data:
        topics = data["data"]
        print(f"    Retrieved {len(topics)} topics")
        return topics
    return []


def parse_iso_date(date_string):
    """Parse ISO 8601 date string to datetime object"""
    try:
        # Handle timezone offset format
        if date_string:
            # Remove microseconds if present
            if '.' in date_string:
                date_string = date_string.split('.')[0] + date_string.split('.')[-1][-6:]
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except:
        pass
    return datetime.now()


def html_to_text(html_string):
    """Basic HTML tag removal for plain text description"""
    import re
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_string)
    # Decode HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    return text.strip()


def create_rss_feed(all_topics):
    """Generate RSS 2.0 XML from topics"""
    print(f"\nGenerating RSS feed with {len(all_topics)} total topics...")

    # Create RSS root element
    rss = Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

    # Create channel
    channel = SubElement(rss, 'channel')

    # Channel metadata
    title = SubElement(channel, 'title')
    title.text = FEED_TITLE

    link = SubElement(channel, 'link')
    link.text = FEED_LINK

    description = SubElement(channel, 'description')
    description.text = FEED_DESCRIPTION

    language = SubElement(channel, 'language')
    language.text = 'en-us'

    last_build = SubElement(channel, 'lastBuildDate')
    last_build.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

    # Add items (topics)
    for topic in all_topics:
        item = SubElement(channel, 'item')

        # Title
        item_title = SubElement(item, 'title')
        item_title.text = f"[{topic['group_name']}] {topic['subject']}"

        # Link - construct URL to the topic
        item_link = SubElement(item, 'link')
        topic_url = f"https://groups.parkslopeparents.com/g/{topic['group_name'].split('+')[-1]}/topic/{topic['id']}"
        item_link.text = topic_url

        # Description
        item_desc = SubElement(item, 'description')
        summary = html_to_text(topic.get('summary', ''))
        # Truncate summary if too long
        if len(summary) > 500:
            summary = summary[:500] + "..."

        desc_text = f"{summary}\n\n"
        desc_text += f"Posted by: {topic.get('name', 'Unknown')}\n"
        desc_text += f"Messages: {topic.get('num_messages', 0)}\n"
        if topic.get('has_attachments'):
            desc_text += "Has attachments\n"

        item_desc.text = desc_text

        # Publication date
        item_date = SubElement(item, 'pubDate')
        pub_date = parse_iso_date(topic.get('updated') or topic.get('created'))
        item_date.text = pub_date.strftime('%a, %d %b %Y %H:%M:%S %z')

        # GUID (unique identifier)
        guid = SubElement(item, 'guid')
        guid.set('isPermaLink', 'true')
        guid.text = topic_url

        # Author
        author = SubElement(item, 'author')
        author.text = topic.get('name', 'Unknown')

        # Category (group name)
        category = SubElement(item, 'category')
        category.text = topic['group_name']

    # Pretty print XML
    xml_string = minidom.parseString(tostring(rss)).toprettyxml(indent="  ")

    return xml_string


def save_feed(xml_content, filename):
    """Save RSS feed to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"\n✓ RSS feed saved to: {filename}")


def main():
    print("=" * 60)
    print("Groups.io to RSS Feed Generator")
    print("=" * 60)
    print()

    # Get all subscribed groups
    groups = get_subscriptions()

    if not groups:
        print("No groups found or error fetching subscriptions")
        sys.exit(1)

    # Fetch topics from all groups
    all_topics = []

    for group in groups:
        group_id = group['group_id']
        group_name = group['group_name']
        nice_name = group.get('nice_group_name', group_name)

        # Skip groups without archive permission
        if not group.get('perms', {}).get('archives_visible', False):
            print(f"  Skipping {nice_name} (no archive access)")
            continue

        topics = get_topics(group_id, group_name, TOPICS_PER_GROUP)

        # Add group name to each topic for reference
        for topic in topics:
            topic['group_name'] = group_name
            topic['nice_group_name'] = nice_name

        all_topics.extend(topics)

    # Sort all topics by most recent first
    all_topics.sort(key=lambda x: x.get('updated') or x.get('created'), reverse=True)

    # Generate RSS feed
    rss_xml = create_rss_feed(all_topics)

    # Save to file
    save_feed(rss_xml, OUTPUT_FILE)

    print(f"\n{'=' * 60}")
    print("Feed generation complete!")
    print(f"{'=' * 60}")
    print(f"\nYou can now:")
    print(f"  1. Open {OUTPUT_FILE} in any RSS reader")
    print(f"  2. Run a simple web server to serve it:")
    print(f"     python3 -m http.server 8000")
    print(f"     Then add: http://localhost:8000/{OUTPUT_FILE} to your RSS reader")
    print(f"  3. Set up a cron job to regenerate this feed periodically")
    print()


if __name__ == "__main__":
    main()
