import requests
import os
from dotenv import load_dotenv
import yaml

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('NOTION_API_KEY')
page_id = "d7513d0a-cdeb-4999-8efb-a5196b2483dc"  # The ID of the page to retrieve

# URL for fetching the page metadata
page_url = f"https://api.notion.com/v1/pages/{page_id}"
# URL for fetching the content blocks
blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Fetch page metadata
response_page = requests.get(page_url, headers=headers)
# Fetch content blocks
response_blocks = requests.get(blocks_url, headers=headers)

if response_page.status_code == 200 and response_blocks.status_code == 200:
    data_page = response_page.json()
    data_blocks = response_blocks.json()

    # Extract metadata and convert it to YAML front matter
    metadata = {
        "id": data_page["id"],
        "created_time": data_page["created_time"],
        "last_edited_time": data_page["last_edited_time"],
        "properties": data_page["properties"]
    }
    yaml_metadata = yaml.dump(metadata, default_flow_style=False)

    # Prepare the markdown content
    page_title = data_page["properties"]["Journal Date"]["title"][0]["plain_text"]
    markdown_content = f"---\n{yaml_metadata}---\n\n# {page_title}\n\n"

    # Parse content blocks
    def parse_block(block):
        block_type = block["type"]
        block_content = ""
        if block_type == "paragraph":
            block_content = block[block_type]["text"][0]["plain_text"] if block[block_type].get("text") else ""
        elif block_type == "heading_1":
            block_content = f"# {block[block_type]['text'][0]['plain_text']}" if block[block_type].get("text") else ""
        elif block_type == "heading_2":
            block_content = f"## {block[block_type]['text'][0]['plain_text']}" if block[block_type].get("text") else ""
        elif block_type == "heading_3":
            block_content = f"### {block[block_type]['text'][0]['plain_text']}" if block[block_type].get("text") else ""
        elif block_type == "bulleted_list_item":
            block_content = f"- {block[block_type]['text'][0]['plain_text']}" if block[block_type].get("text") else ""
        elif block_type == "numbered_list_item":
            block_content = f"1. {block[block_type]['text'][0]['plain_text']}" if block[block_type].get("text") else ""
        elif block_type == "to_do":
            checked = block[block_type]["checked"]
            block_content = f"- [ {'x' if checked else ' '} ] {block[block_type]['text'][0]['plain_text']}" if block[block_type].get("text") else ""
        # Add more block types as needed
        return block_content

    for block in data_blocks["results"]:
        markdown_content += parse_block(block) + "\n\n"

    # Save the markdown file
    output_dir = os.path.join(os.getcwd(), "test")
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f"{page_title}.md")

    with open(output_file_path, "w") as md_file:
        md_file.write(markdown_content)

    print(f"Markdown file created: {output_file_path}")
else:
    print(f"Failed to retrieve the page or blocks. Status codes: {response_page.status_code}, {response_blocks.status_code}")
