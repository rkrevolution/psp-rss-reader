# Groups.io API Guide: Getting Recent Topics

This guide shows you how to use the groups.io API to retrieve recent topics from your subscribed groups.

## Prerequisites

- A groups.io account
- An API key (64-character string)
- `curl` command-line tool (pre-installed on macOS/Linux)

## Authentication

The groups.io API uses Bearer token authentication. Include your API key in the `Authorization` header:

```bash
Authorization: Bearer YOUR_64_CHARACTER_API_KEY
```

## API Base URL

All API endpoints use the base URL:
```
https://groups.io/api/v1/
```

## Step 1: Get Your Subscribed Groups

Before you can get topics, you need to know your group IDs.

### Endpoint
```
GET https://groups.io/api/v1/getsubs
```

### Example Request
```bash
curl -s -H "Authorization: Bearer YOUR_API_KEY" \
  "https://groups.io/api/v1/getsubs"
```

### Example Response
```json
{
  "object": "list",
  "total_count": 5,
  "data": [
    {
      "id": 14823442,
      "group_id": 8395,
      "group_name": "parkslopeparents",
      "nice_group_name": "Groups.io | Advice",
      "subs_count": 11586,
      "most_recent_message": "2026-01-12T19:35:47.039715378-08:00",
      "perms": {
        "archives_visible": true,
        ...
      }
    },
    ...
  ]
}
```

### Key Fields
- `group_id`: The numeric ID you'll use to query topics
- `group_name`: The group's identifier name
- `nice_group_name`: Human-readable display name
- `perms.archives_visible`: Must be `true` to access topics

## Step 2: Get Recent Topics from a Group

Once you have a `group_id`, you can retrieve topics.

### Endpoint
```
GET https://groups.io/api/v1/gettopics
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_id` | integer | Yes | The numeric group ID from step 1 |
| `limit` | integer | No | Number of topics to return (default: 100) |
| `next_page_token` | integer | No | For pagination - get next page of results |

### Example Request: Get 10 Most Recent Topics

```bash
curl -s -H "Authorization: Bearer YOUR_API_KEY" \
  "https://groups.io/api/v1/gettopics?group_id=8395&limit=10"
```

### Example Response
```json
{
  "object": "list",
  "total_count": 217825,
  "start_item": 1,
  "end_item": 10,
  "has_more": true,
  "next_page_token": 1768251011301721253,
  "sort_field": "recentpostdate/sticky",
  "sort_dir": "desc",
  "data": [
    {
      "id": 117238076,
      "object": "topic",
      "created": "2026-01-12T19:35:47.043922965-08:00",
      "updated": "2026-01-12T19:35:47.043922965-08:00",
      "group_id": 8395,
      "subject": "MLK Day of Service--",
      "summary": "We're putting together this weeks Picks Newsletter...",
      "name": "Susan Fox",
      "num_messages": 1,
      "is_sticky": false,
      "is_moderated": false,
      "is_closed": false,
      "has_attachments": true,
      "most_recent_message": "2026-01-12T19:35:47.039715378-08:00"
    },
    ...
  ]
}
```

### Response Fields

**List Metadata:**
- `total_count`: Total number of topics in the group
- `start_item` / `end_item`: Range of items in current response
- `has_more`: Whether there are more pages available
- `next_page_token`: Token to use for next page (if `has_more` is true)

**Topic Data:**
- `id`: Unique topic ID
- `subject`: Topic title/subject line
- `summary`: Preview of the topic content
- `name`: Name of topic creator
- `num_messages`: Number of messages in the thread
- `is_sticky`: Whether topic is pinned to top
- `has_attachments`: Whether topic contains attachments
- `created`: When topic was created (ISO 8601 format)
- `updated`: Last update time
- `most_recent_message`: Timestamp of most recent message

## Step 3: Pagination (Getting More Topics)

If `has_more` is `true`, use the `next_page_token` to get the next page:

```bash
curl -s -H "Authorization: Bearer YOUR_API_KEY" \
  "https://groups.io/api/v1/gettopics?group_id=8395&limit=10&next_page_token=1768251011301721253"
```

## Formatting JSON Output

To make the JSON response more readable, pipe it through `python3 -m json.tool` or `jq`:

```bash
# Using Python (pre-installed on macOS)
curl -s -H "Authorization: Bearer YOUR_API_KEY" \
  "https://groups.io/api/v1/gettopics?group_id=8395&limit=10" | python3 -m json.tool

# Using jq (if installed)
curl -s -H "Authorization: Bearer YOUR_API_KEY" \
  "https://groups.io/api/v1/gettopics?group_id=8395&limit=10" | jq
```

## Complete Example Script

Save this as `get_topics.sh`:

```bash
#!/bin/bash

# Configuration
API_KEY="YOUR_64_CHARACTER_API_KEY_HERE"
GROUP_ID="8395"
LIMIT="10"

# Make the API call
curl -s -H "Authorization: Bearer $API_KEY" \
  "https://groups.io/api/v1/gettopics?group_id=$GROUP_ID&limit=$LIMIT" \
  | python3 -m json.tool
```

Make it executable and run:
```bash
chmod +x get_topics.sh
./get_topics.sh
```

## Permissions Required

To use the `gettopics` endpoint, you must have:
- `archives_visible` permission set to `true` for that group
- This permission is shown in the `perms` object when you call `getsubs`

## Error Handling

Common errors:

- **404 page not found**: Wrong endpoint URL (make sure to use `/api/v1/` not `/v1/`)
- **401 Unauthorized**: Invalid or expired API key
- **403 Forbidden**: You don't have permission to view archives for this group
- Empty response: Check that the group_id is correct

## API Resources

- Official API Documentation: https://groups.io/api
- API Keys Help: https://groups.io/helpcenter/manual/membersmanual/accounts/accounts_API_keys.htm
- API Access Guide: https://groups.io/helpcenter/ownersmanual/1/additional-information/api-access-and-documentation

## Notes

- API keys provide full access equivalent to logging in
- Store your API key securely (use environment variables, not hardcoded in scripts)
- The API is actively under development and may change
- All requests must use HTTPS
- Topics are sorted by most recent post date by default, with sticky topics first
