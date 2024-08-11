import requests
import os
from dotenv import load_dotenv
import yaml

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('NOTION_API_KEY')
page_id = "d7513d0a-cdeb-4999-8efb-a5196b2483dc"

# URL for fetching the page metadata
page_url = f"https://api.notion.com/v1/pages/{page_id}"
# URL for fetching the content blocks
blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}   

response_page = requests.get(page_url, headers=headers)
response_blocks = requests.get(blocks_url, headers=headers)

if response_page.status_code == 200 and response_blocks.status_code == 200:
    data_page = response_page.json()
    data_blocks = response_blocks.json()

    # Print out the data_blocks to see its structure (for debugging)
    print(data_blocks)
