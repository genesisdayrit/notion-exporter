import os
import shutil

# Define the path to the file containing the mappings
mappings_file = 'mappings.txt'

# Define the path for resolving conflicts
resolve_conflicts_path = '/Users/Genesis/Dropbox/obsidian/personal/resolve-conflicts'

# Ensure the resolve-conflicts directory exists
os.makedirs(resolve_conflicts_path, exist_ok=True)

# Read the mappings from the file
with open(mappings_file, 'r') as file:
    mappings = file.read().splitlines()

# Loop through each mapping in the file
for mapping in mappings:
    # Ignore lines that are empty or start with '#'
    if not mapping.strip() or mapping.startswith('#'):
        continue

    # Split the mapping by the tab character '\t'
    source_path, destination_path = mapping.split('\t')

    if not os.path.exists(source_path):
        print(f"The source path {source_path} does not exist.")
        continue
    if not os.path.exists(destination_path):
        print(f"The destination path {destination_path} does not exist.")
        continue

    # Loop through all files in the source directory
    for file in os.listdir(source_path):
        source_file_path = os.path.join(source_path, file)
        destination_file_path = os.path.join(destination_path, file)

        # Check if the file already exists in the destination
        if os.path.exists(destination_file_path):
            # Modify the file name to include ' (notion)' before the extension
            file_name, file_extension = os.path.splitext(file)
            conflict_file_name = f"{file_name} (notion){file_extension}"
            resolve_file_path = os.path.join(resolve_conflicts_path, conflict_file_name)

            # Move the conflicting file to the resolve-conflicts directory
            shutil.move(source_file_path, resolve_file_path)
            print(f"File {file} already exists in {destination_path}. Moved to resolve-conflicts as {conflict_file_name}.")
        else:
            # Move the file to the destination directory
            shutil.move(source_file_path, destination_file_path)

    print(f"All files have been successfully moved from {source_path} to {destination_path}.")
