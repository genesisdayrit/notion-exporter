import os
import shutil
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the base path from the environment variable
base_path = os.getenv("NOTION_IMPORTER_CLEANUP_PATH")

# Define the 'Journal' directory path
journal_path = os.path.join(base_path, "Journal")

if not os.path.exists(journal_path):
    raise ValueError(f"The path {journal_path} does not exist.")

# Loop through all entries in the Journal directory
for root, dirs, files in os.walk(journal_path, topdown=False):
    for file in files:
        # Construct full file path
        file_path = os.path.join(root, file)
        # Move the file to the Journal directory
        shutil.move(file_path, os.path.join(journal_path, file))

    # After moving files, remove the now-empty directories
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if not os.listdir(dir_path):  # Check if the directory is empty
            os.rmdir(dir_path)

print("All files have been moved to the Journal directory, and empty subfolders have been removed.")
