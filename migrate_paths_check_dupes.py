import os
import shutil
import logging

# Set up logging
logging.basicConfig(
    filename='migration_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define the path to the file containing the mappings
mappings_file = 'mappings.txt'

# Define the base vault path and resolve-conflicts directory
vault_base_path = '/Users/Genesis/Dropbox/obsidian/personal'
resolve_conflicts_path = os.path.join(vault_base_path, 'resolve-conflicts')

# Ensure the resolve-conflicts directory exists
os.makedirs(resolve_conflicts_path, exist_ok=True)

# Read the mappings from the file
with open(mappings_file, 'r') as file:
    mappings = file.read().splitlines()

# Function to check if a file exists anywhere in the vault
def check_file_exists_globally(file_name, vault_base_path):
    for root, dirs, files in os.walk(vault_base_path):
        if file_name in files:
            return True
    return False

# Loop through each mapping in the file
for mapping in mappings:
    # Ignore lines that are empty or start with '#'
    if not mapping.strip() or mapping.startswith('#'):
        continue

    # Split the mapping by the tab character '\t'
    source_path, destination_path = mapping.split('\t')

    if not os.path.exists(source_path):
        logging.warning(f"The source path {source_path} does not exist.")
        continue
    if not os.path.exists(destination_path):
        logging.warning(f"The destination path {destination_path} does not exist.")
        continue

    # Loop through all files in the source directory
    for file in os.listdir(source_path):
        source_file_path = os.path.join(source_path, file)
        destination_file_path = os.path.join(destination_path, file)

        # Check if the file exists anywhere in the vault
        if check_file_exists_globally(file, vault_base_path):
            # Modify the file name to include ' (notion)' before the extension
            file_name, file_extension = os.path.splitext(file)
            conflict_file_name = f"{file_name} (notion){file_extension}"
            resolve_file_path = os.path.join(resolve_conflicts_path, conflict_file_name)

            # Move the conflicting file to the resolve-conflicts directory
            shutil.move(source_file_path, resolve_file_path)
            logging.info(f"File {file} already exists in the vault. Moved to resolve-conflicts as {conflict_file_name}.")
        else:
            # Move the file to the destination directory
            shutil.move(source_file_path, destination_file_path)
            logging.info(f"Moved file {file} from {source_path} to {destination_path}.")

    logging.info(f"Completed processing for {source_path}.")

logging.info("All mappings have been processed.")
print("Migration complete. Check migration_log.txt for details.")
