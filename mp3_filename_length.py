import os

# Set the root directory where the mp3 files are located
root_dir = 'C:/Users/jakub/Desktop/br_update_files_namechange'

# Loop through all the directories and subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Loop through all the files in the current directory
    for filename in filenames:
        # Check if the file is a mp3 file
        if filename.endswith('.mp3'):
            # Check if the filename length (without ".mp3" suffix) is exactly 25 characters
            if len(filename) - len('.mp3') <= 25:
                # Print the filename without the ".mp3" suffix
                print(filename[:-4])
            else:
                print("No filenames equal or under 25 chars.")
