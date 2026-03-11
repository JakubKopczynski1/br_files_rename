import os
import shutil
import sys
import pandas as pd

root_dir = 'C:/Users/jakub/Desktop/br_update'

mapping_file = 'C:/Users/jakub/Desktop/br_file_rename2 update.csv'
mapping_df = pd.read_csv(mapping_file)
mapping_dict = dict(zip(mapping_df['old_filename'], mapping_df['new_filename']))

renamed_count = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.mp3'):
            old_path = os.path.join(dirpath, filename)

            try:
                if filename in mapping_dict:
                    new_filename = mapping_dict[filename]
                    new_path = os.path.join(dirpath, new_filename)

                    shutil.move(old_path, new_path)

                    renamed_count += 1
                    sys.stdout.write(f'\rFiles renamed: {renamed_count}')
                    sys.stdout.flush()

            except Exception as e:
                print(f'\nError renaming {filename}: {e}')

print(f'\nFinished! Total MP3 files renamed: {renamed_count}')
