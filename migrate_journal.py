import os
import shutil
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the base paths from the environment variables
source_base_path = os.getenv("NOTION_IMPORTER_CLEANUP_PATH")
destination_base_path = os.getenv("DESTINATION_OBSIDIAN_VAULT_PATH")

# Define the 'Journal' directory paths
source_journal_path = os.path.join(source_base_path, "Journal")
destination_journal_path = os.path.join(destination_base_path, "01_Daily", "_Journal")

if not os.path.exists(source_journal_path):
    raise ValueError(f"The source path {source_journal_path} does not exist.")
if not os.path.exists(destination_journal_path):
    raise ValueError(f"The destination path {destination_journal_path} does not exist.")

# Loop through all files in the source Journal directory
for file in os.listdir(source_journal_path):
    source_file_path = os.path.join(source_journal_path, file)
    destination_file_path = os.path.join(destination_journal_path, file)
    
    # Move the file to the destination Journal directory
    shutil.move(source_file_path, destination_file_path)

print(f"All files have been successfully moved from {source_journal_path} to {destination_journal_path}.")
