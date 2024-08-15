import os

def count_files_folders_and_size(directory):
    total_files = 0
    total_folders = 0
    total_size = 0

    for root, dirs, files in os.walk(directory):
        total_folders += len(dirs)
        total_files += len(files)
        total_size += sum(os.path.getsize(os.path.join(root, file)) for file in files)

    return total_files, total_folders, total_size

def format_size(size):
    # Convert size to a more readable format (bytes, KB, MB, GB, etc.)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

directory_path = "/Users/Genesis/obsidian/notion-export/raw-export/notion-full-export-2024-08-11"

files, folders, size = count_files_folders_and_size(directory_path)
if __name__ == "__main__":
    files, folders, size = count_files_folders_and_size(directory_path)
    print(f"Notion Export:")
    print(f"Total files: {files}")
    # print(f"Total folders: {folders}")
    print(f"Total size: {format_size(size)}")
