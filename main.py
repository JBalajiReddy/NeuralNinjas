import os
import requests
from datetime import datetime, timezone

# Retrieve environment variables
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

# Check if environment variables are set
if NOTION_TOKEN is None or DATABASE_ID is None:
    raise ValueError("Environment variables NOTION_TOKEN and DATABASE_ID must be set.")

# API headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Functions to interact with Notion API
def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    if res.status_code != 200:
        print(f"Error creating page: {res.status_code}")
        print(res.json())
    return res

# Example data to create a page
title = "Test Title"
description = "Test Description"
published_date = datetime.now().astimezone(timezone.utc).isoformat()
data = {
    "URL": {"title": [{"text": {"content": description}}]},
    "Title": {"rich_text": [{"text": {"content": title}}]},
    "Published": {"date": {"start": published_date, "end": None}}
}

# Create a page
create_page(data)

# Function to retrieve pages from the database
def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Error retrieving pages: {response.status_code}")
        print(response.json())
        return []

    data = response.json()
    results = data["results"]
    while data.get("has_more") and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Error retrieving pages: {response.status_code}")
            print(response.json())
            break
        data = response.json()
        results.extend(data["results"])

    return results

# Example usage: Retrieve pages
pages = get_pages()

for page in pages:
    page_id = page["id"]
    props = page["properties"]
    url = props["URL"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    published = props["Published"]["date"]["start"]
    published = datetime.fromisoformat(published)

    print(f"Page ID: {page_id}")
    print(f"URL: {url}")
    print(f"Title: {title}")
    print(f"Published: {published}")

# Function to update a page
def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": data}
    res = requests.patch(url, json=payload, headers=headers)
    if res.status_code != 200:
        print(f"Error updating page: {res.status_code}")
        print(res.json())
    return res

# Example usage: Update a page
page_id = "YOUR_PAGE_ID"
new_date = datetime(2023, 1, 15).astimezone(timezone.utc).isoformat()
update_data = {"Published": {"date": {"start": new_date, "end": None}}}

update_page(page_id, update_data)

# Function to delete a page
def delete_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": True}
    res = requests.patch(url, json=payload, headers=headers)
    if res.status_code != 200:
        print(f"Error deleting page: {res.status_code}")
        print(res.json())
    return res

# Example usage: Delete a page
delete_page(page_id)
