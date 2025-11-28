import os
import shutil

# Source directory (where all your folders with MP3 files are)
source_dir = 'C:/Users/jakub/Desktop/br_update_files_namechange'

# Destination directory (where you want to move all the MP3 files)
destination_dir = 'C:/Users/jakub/Desktop/br_update_files_short'

# Ensure the destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Initialize counter for moved files
moved_count = 0

# Step 1: Walk through each folder and subfolder in the source directory
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # Step 2: Check if the file has a .mp3 extension
        if file.lower().endswith('.mp3'):
            # Step 3: Get the full file path
            file_path = os.path.join(root, file)

            # Step 4: Move the file to the destination directory
            try:
                shutil.move(file_path, destination_dir)
            except Exception as e:
                print(f'Error moving {file}: {e}')
            # Increment counter for renamed files
            moved_count += 1

print("Total MP3 files moved:", moved_count)
