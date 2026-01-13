#!/usr/bin/env python3
"""
Groups.io RSS Feed Server

A simple web server that serves a dynamically-generated RSS feed
from your groups.io subscriptions.

Usage:
    python3 rss_server.py [port]

Default port: 8000

Access your feed at: http://localhost:8000/feed.xml
"""

import http.server
import socketserver
import threading
import time
import sys
from pathlib import Path

# Import the feed generator
import generate_rss_feed as rss_gen

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
REFRESH_INTERVAL = 1800  # Refresh every 30 minutes (1800 seconds)


class RSSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler that serves the RSS feed"""

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/feed.xml' or self.path == '/':
            # Serve the feed
            self.path = '/feed.xml'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/refresh':
            # Manual refresh endpoint
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Refreshing feed...\n')
            generate_feed()
            self.wfile.write(b'Feed refreshed!\n')
        else:
            # Serve other files normally
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def generate_feed():
    """Generate the RSS feed"""
    try:
        print("\n" + "=" * 60)
        print("Refreshing RSS feed...")
        print("=" * 60)

        # Get subscriptions
        groups = rss_gen.get_subscriptions()

        if not groups:
            print("No groups found")
            return

        # Fetch topics
        all_topics = []
        for group in groups:
            group_id = group['group_id']
            group_name = group['group_name']

            if not group.get('perms', {}).get('archives_visible', False):
                continue

            topics = rss_gen.get_topics(group_id, group_name, rss_gen.TOPICS_PER_GROUP)

            for topic in topics:
                topic['group_name'] = group_name
                topic['nice_group_name'] = group.get('nice_group_name', group_name)

            all_topics.extend(topics)

        # Sort by most recent
        all_topics.sort(key=lambda x: x.get('updated') or x.get('created'), reverse=True)

        # Generate and save
        rss_xml = rss_gen.create_rss_feed(all_topics)
        rss_gen.save_feed(rss_xml, rss_gen.OUTPUT_FILE)

        print(f"\n✓ Feed refreshed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"Error generating feed: {e}")


def auto_refresh_feed():
    """Periodically refresh the feed in the background"""
    while True:
        time.sleep(REFRESH_INTERVAL)
        generate_feed()


def main():
    # Generate initial feed
    print("=" * 60)
    print("Groups.io RSS Feed Server")
    print("=" * 60)
    print()
    generate_feed()

    # Start background refresh thread
    refresh_thread = threading.Thread(target=auto_refresh_feed, daemon=True)
    refresh_thread.start()
    print(f"\n✓ Auto-refresh enabled (every {REFRESH_INTERVAL // 60} minutes)")

    # Start web server
    Handler = RSSRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n{'=' * 60}")
        print(f"Server running on http://localhost:{PORT}")
        print(f"{'=' * 60}")
        print(f"\n📡 RSS Feed URL: http://localhost:{PORT}/feed.xml")
        print(f"🔄 Manual refresh: http://localhost:{PORT}/refresh")
        print(f"\nAdd this URL to your RSS reader:")
        print(f"  http://localhost:{PORT}/feed.xml")
        print(f"\nPress Ctrl+C to stop the server")
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()


if __name__ == "__main__":
    main()
