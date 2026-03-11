import os
import shutil
import sys

files_dir = 'C:/Users/jakub/Desktop/br_update'
albums_dir = 'C:/Users/jakub/Desktop/br_album_folders'

# Build dictionary of album folders
album_dirs = {}

for item in os.listdir(albums_dir):
    full_path = os.path.join(albums_dir, item)
    if os.path.isdir(full_path):
        key = "_".join(item.split("_")[:2])
        album_dirs[key] = full_path

moved_count = 0
not_found = 0

for filename in os.listdir(files_dir):
    if filename.lower().endswith(".mp3"):

        file_path = os.path.join(files_dir, filename)

        try:
            key = "_".join(filename.split("_")[:2])

            if key in album_dirs:
                destination = os.path.join(album_dirs[key], filename)

                shutil.move(file_path, destination)

                moved_count += 1
                sys.stdout.write(f'\rFiles moved: {moved_count}')
                sys.stdout.flush()

            else:
                print(f"\nNo folder for: {filename}")
                not_found += 1

        except Exception as e:
            print(f"\nError moving {filename}: {e}")

print(f"\nFinished!")
print(f"Files moved: {moved_count}")
print(f"Files without matching folder: {not_found}")