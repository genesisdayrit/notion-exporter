import os
import shutil

# Define the path to the file containing the paths to clean
paths_file = 'paths_to_clean.txt'

# Read the paths from the file
with open(paths_file, 'r') as file:
    paths_to_clean = file.read().splitlines()

# Loop through each path in the file
for base_path in paths_to_clean:
    if not os.path.exists(base_path):
        print(f"The path {base_path} does not exist.")
        continue

    # Loop through all entries in the current path directory
    for root, dirs, files in os.walk(base_path, topdown=False):
        for file in files:
            # Construct full file path
            file_path = os.path.join(root, file)
            # Move the file to the base path directory
            shutil.move(file_path, os.path.join(base_path, file))

        # After moving files, remove the now-empty directories
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # Check if the directory is empty
                os.rmdir(dir_path)

    print(f"All files have been moved to the directory {base_path}, and empty subfolders have been removed.")
