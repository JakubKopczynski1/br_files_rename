import os

root_dir = 'C:/Users/jakub/Desktop/br_update'

problem_files = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.mp3'):
            name, ext = os.path.splitext(filename)

            if len(name) > 25:
                print(filename)
                problem_files += 1

print(f"\nFiles still longer than 25 characters: {problem_files}")