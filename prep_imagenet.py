import os
import shutil
from tqdm import tqdm

def organize_imagenet():
    source_dir = '/workspace/imagenet-1k/data/train'
    target_dir = '/workspace/imagenet-1k/train/'

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Get all subdirectories in the source directory
    subdirs = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

    for subdir in subdirs:
        current_source_dir = os.path.join(source_dir, subdir)

        # Ensure the current target directory exists
        os.makedirs(target_dir, exist_ok=True)

        # Get all files in the current source directory
        files = [f for f in os.listdir(current_source_dir) if f.endswith('.JPEG')]

        for file in tqdm(files, desc=f"Organizing files in {subdir}"):
            # Split the filename to get the synset_id
            filename, _ = os.path.splitext(file)
            _, synset_id = filename.rsplit('_', 1)

            # Create the synset directory if it doesn't exist
            synset_dir = os.path.join(target_dir, synset_id)
            os.makedirs(synset_dir, exist_ok=True)

            # Construct the new filename
            new_filename = f"{filename.rsplit('_', 1)[0]}.jpeg"

            # Move and rename the file
            src_path = os.path.join(current_source_dir, file)
            dst_path = os.path.join(synset_dir, new_filename)
            shutil.copy(src_path, dst_path)

if __name__ == "__main__":
    organize_imagenet()
    print("ImageNet organization complete.")
