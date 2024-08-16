import os
import shutil
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the path from the environment variable
path = os.getenv("NOTION_IMPORTER_CLEANUP_PATH")

if not path:
    raise ValueError("Environment variable NOTION_IMPORTER_CLEANUP_PATH is not set.")

# Define the 'other' directory path
other_dir = os.path.join(path, "other")

# Create the 'other' directory if it doesn't exist
os.makedirs(other_dir, exist_ok=True)

# Get a list of all files and directories in the directory
entries = os.listdir(path)

# Loop through all entries
for entry in entries:
    # Create the full path for each entry
    full_path = os.path.join(path, entry)

    # Skip if it's a directory
    if os.path.isdir(full_path):
        continue

    # Split the file name and extension
    _, ext = os.path.splitext(entry)

    # Clean up the extension (remove leading dot)
    ext = ext.lstrip(".")

    # Create a subdirectory for the file extension within the 'other' directory
    ext_dir = os.path.join(other_dir, ext)
    os.makedirs(ext_dir, exist_ok=True)

    # Move the file to the appropriate subdirectory
    shutil.move(full_path, os.path.join(ext_dir, entry))

print("Files have been successfully organized into the 'other' directory.")
