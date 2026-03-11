import os
import shutil
import sys

source_dir = 'C:/Users/jakub/Desktop/br_harvest_downloads/files'
destination_dir = 'C:/Users/jakub/Desktop/br_update'

os.makedirs(destination_dir, exist_ok=True)

moved_count = 0

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith('.mp3'):
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_dir, file)

            try:
                shutil.move(source_path, destination_path)

                moved_count += 1
                sys.stdout.write(f'\rFiles moved: {moved_count}')
                sys.stdout.flush()

            except Exception as e:
                print(f'\nError moving {file}: {e}')

print(f'\nFinished! Total MP3 files moved: {moved_count}')