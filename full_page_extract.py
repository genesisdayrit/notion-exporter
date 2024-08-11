import requests
import os
from dotenv import load_dotenv
import yaml

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('NOTION_API_KEY')
page_id = os.getenv('NOTION_PAGE_ID')

# API URLs
NOTION_API_URL = "https://api.notion.com/v1"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Fetch the page metadata
def fetch_page_metadata(page_id):
    url = f"{NOTION_API_URL}/pages/{page_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Fetch the blocks from a Notion page
def fetch_blocks(page_id, start_cursor=None):
    url = f"{NOTION_API_URL}/blocks/{page_id}/children"
    params = {"page_size": 100}
    if start_cursor:
        params["start_cursor"] = start_cursor
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Recursive function to parse blocks into Markdown format
def parse_block(block, indent_level=0):
    block_type = block["type"]
    markdown_content = ""

    if block_type == "paragraph":
        markdown_content = parse_paragraph(block)
    elif block_type.startswith("heading_"):
        markdown_content = parse_heading(block, block_type)
    elif block_type == "bulleted_list_item":
        markdown_content = parse_list_item(block, "- ", indent_level)
    elif block_type == "numbered_list_item":
        markdown_content = parse_list_item(block, "1. ", indent_level)
    elif block_type == "to_do":
        markdown_content = parse_to_do(block, indent_level)
    elif block_type == "quote":
        markdown_content = parse_quote(block)
    elif block_type == "code":
        markdown_content = parse_code(block)
    elif block_type == "divider":
        markdown_content = "---\n"
    elif block_type == "image":
        markdown_content = parse_image(block)
    elif block_type == "callout":
        markdown_content = parse_callout(block)
    elif block_type == "toggle":
        markdown_content = parse_toggle(block, indent_level)

    # Handle nested blocks (children)
    if block.get("has_children"):
        child_blocks = fetch_blocks(block["id"])
        for child in child_blocks["results"]:
            markdown_content += parse_block(child, indent_level + 1)

    return markdown_content

# Helper functions for each block type
def parse_paragraph(block):
    text = extract_text(block["paragraph"]["rich_text"])
    return f"{text}\n\n"

def parse_heading(block, block_type):
    text = extract_text(block[block_type]["rich_text"])
    level = block_type.split("_")[-1]
    return f"{'#' * int(level)} {text}\n\n"

def parse_list_item(block, prefix, indent_level):
    text = extract_text(block[block["type"]]["rich_text"])
    indent = "  " * indent_level
    return f"{indent}{prefix}{text}\n"

def parse_to_do(block, indent_level):
    checked = block["to_do"]["checked"]
    text = extract_text(block["to_do"]["rich_text"])
    indent = "  " * indent_level
    checkbox = "[x]" if checked else "[ ]"
    return f"{indent}- {checkbox} {text}\n"

def parse_quote(block):
    text = extract_text(block["quote"]["rich_text"])
    return f"> {text}\n\n"

def parse_code(block):
    code = block["code"]["rich_text"][0]["text"]["content"]
    language = block["code"].get("language", "")
    return f"```{language}\n{code}\n```\n\n"

def parse_image(block):
    image_url = block["image"].get("file", {}).get("url", block["image"].get("external", {}).get("url", ""))
    return f"![Image]({image_url})\n\n"

def parse_callout(block):
    icon = block["callout"].get("icon", {}).get("emoji", "")
    text = extract_text(block["callout"]["rich_text"])
    return f"> {icon} {text}\n\n"

def parse_toggle(block, indent_level):
    text = extract_text(block["toggle"]["rich_text"])
    indent = "  " * indent_level
    toggle_content = f"{indent}* {text}\n"
    if block.get("has_children"):
        toggle_content += parse_block_children(block["id"], indent_level + 1)
    return toggle_content

def extract_text(rich_text_array):
    text = ""
    for rich_text in rich_text_array:
        if 'text' in rich_text:
            plain_text = rich_text["text"]["content"]
            annotations = rich_text["annotations"]
            if annotations.get("bold"):
                plain_text = f"**{plain_text}**"
            if annotations.get("italic"):
                plain_text = f"*{plain_text}*"
            if annotations.get("strikethrough"):
                plain_text = f"~~{plain_text}~~"
            if annotations.get("underline"):
                plain_text = f"<u>{plain_text}</u>"
            if annotations.get("code"):
                plain_text = f"`{plain_text}`"
            if rich_text["text"].get("link"):
                url = rich_text["text"]["link"]["url"]
                plain_text = f"[{plain_text}]({url})"
            text += plain_text
        elif 'mention' in rich_text and rich_text['mention']['type'] == 'page':
            # Handling Notion page links
            page_id = rich_text['mention']['page']['id']
            page_name = rich_text['plain_text']
            text += f"[[{page_name}]]"
    return text

# Fetch children of a block (for nested blocks)
def parse_block_children(block_id, indent_level):
    child_blocks = fetch_blocks(block_id)
    markdown_content = ""
    for child in child_blocks["results"]:
        markdown_content += parse_block(child, indent_level)
    return markdown_content

# Main function to process the page and generate Markdown
def generate_markdown(page_id):
    # Fetch the page metadata and blocks
    data_page = fetch_page_metadata(page_id)
    blocks = fetch_blocks(page_id)

    # Extract metadata and convert it to YAML front matter
    metadata = {
        "id": data_page["id"],
        "created_time": data_page["created_time"],
        "last_edited_time": data_page["last_edited_time"],
        "properties": data_page["properties"]
    }
    yaml_metadata = yaml.dump(metadata, default_flow_style=False)

    # Extract the page title
    page_title = data_page["properties"]["Journal Date"]["title"][0]["plain_text"]

    # Prepare the markdown content
    markdown_content = f"---\n{yaml_metadata}---\n\n# {page_title}\n\n"

    # Parse content blocks
    for block in blocks["results"]:
        markdown_content += parse_block(block)

    # Save the markdown file
    output_dir = os.path.join(os.getcwd(), "test")
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f"{page_title}.md")

    with open(output_file_path, "w") as md_file:
        md_file.write(markdown_content)

    print(f"Markdown file created: {output_file_path}")

if __name__ == "__main__":
    generate_markdown(page_id)
