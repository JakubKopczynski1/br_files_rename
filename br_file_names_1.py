import os
import shutil

# Set the root directory where the mp3 files are located
root_dir = 'C:/Users/jakub/Desktop/br_update_files_short'

# Initialize counter for renamed files
renamed_count = 0

# Loop through all the directories and subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Loop through all the files in the current directory
    for filename in filenames:
        # Check if the file is a mp3 file
        if filename.endswith('.mp3'):
            # Construct the old and new file names
            old_path = os.path.join(dirpath, filename)
            # We have to cut the file name to 25 first characters, because Harvest doesn't produce full file names
            # But cuts them to 120 characters, and then they don't match names in metadata
            new_filename = filename[:25] + '.mp3'
            new_path = os.path.join(dirpath, new_filename)
            # Rename the file
            shutil.move(old_path, new_path)
            # Increment counter for renamed files
            renamed_count += 1

# Print the number of renamed files
print("Total MP3 files renamed:", renamed_count)
