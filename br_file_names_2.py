import os
import shutil
import pandas as pd

# Set the root directory where the mp3 files are located
root_dir = 'C:/Users/jakub/Desktop/br_update_files_short'

# Load the Excel file with the file name mappings into a pandas DataFrame
mapping_file = 'C:/Users/jakub/Desktop/20250327 br_file_rename2 update.xlsx'
mapping_df = pd.read_excel(mapping_file)

# Initialize counter for renamed files
renamed_count = 0

# Loop through all the directories and subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Loop through all the files in the current directory
    for filename in filenames:
        # Check if the file is a mp3 file
        if filename.endswith('.mp3'):
            # Check if the file name is in the mapping DataFrame
            old_filename = os.path.join(dirpath, filename)
            new_filename = mapping_df.loc[mapping_df['old_filename'] == filename, 'new_filename'].values
            if len(new_filename) > 0:
                new_filename = new_filename[0]
                new_path = os.path.join(dirpath, new_filename)
                # Rename the file
                shutil.move(old_filename, new_path)
                # Increment counter for renamed files
                renamed_count += 1

# Print the number of renamed files
print("Total MP3 files renamed:", renamed_count)
