import requests
import os
from dotenv import load_dotenv
import yaml

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('NOTION_API_KEY')
page_id = "d7513d0a-cdeb-4999-8efb-a5196b2483dc"  # The ID of the page to retrieve

url = f"https://api.notion.com/v1/pages/{page_id}"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Make the API request
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    # Extract metadata and convert it to YAML front matter
    metadata = {
        "id": data["id"],
        "created_time": data["created_time"],
        "last_edited_time": data["last_edited_time"],
        "properties": data["properties"]
    }
    yaml_metadata = yaml.dump(metadata, default_flow_style=False)

    # Prepare the markdown content
    page_title = data["properties"]["Journal Date"]["title"][0]["plain_text"]
    markdown_content = f"---\n{yaml_metadata}---\n\n# {page_title}\n\n"

    # Save the markdown file
    output_dir = os.path.join(os.getcwd(), "test")
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f"{page_title}.md")

    with open(output_file_path, "w") as md_file:
        md_file.write(markdown_content)

    print(f"Markdown file created: {output_file_path}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
