import os
import shutil
import sys

root_dir = 'C:/Users/jakub/Desktop/br_update'

trimmed_count = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.mp3'):
            old_path = os.path.join(dirpath, filename)
            # We have to trim the file name to 25 first characters, because Harvest doesn't produce full file names
            # But cuts them to 120 characters, and then they don't match names in metadata
            try:
                new_filename = filename[:25] + '.mp3'
                new_path = os.path.join(dirpath, new_filename)

                if old_path == new_path:
                    continue

                shutil.move(old_path, new_path)

                trimmed_count += 1
                sys.stdout.write(f'\rFiles trimmed: {trimmed_count}')
                sys.stdout.flush()
            except Exception as e:
                print(f'\nError trimming {filename}: {e}')

print(f'\nFinished! Total MP3 files trimmed: {trimmed_count}')
