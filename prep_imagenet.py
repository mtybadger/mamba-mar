import os
import shutil
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_file(args):
    source_dir, target_dir, subdir, file = args
    # ... existing file processing logic ...
    src_path = os.path.join(source_dir, subdir, file)
    filename, _ = os.path.splitext(file)
    _, synset_id = filename.rsplit('_', 1)
    synset_dir = os.path.join(target_dir, synset_id)
    new_filename = f"{filename.rsplit('_', 1)[0]}.jpeg"
    dst_path = os.path.join(synset_dir, new_filename)
    os.makedirs(synset_dir, exist_ok=True)
    shutil.copy(src_path, dst_path)

def organize_imagenet():
    source_dir = '/workspace/imagenet-1k/data/train'
    target_dir = '/workspace/imagenet-1k/train/'

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Get all subdirectories in the source directory
    subdirs = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

    with ProcessPoolExecutor() as executor:
        futures = []
        for subdir in subdirs:
            current_source_dir = os.path.join(source_dir, subdir)
            files = [f for f in os.listdir(current_source_dir) if f.endswith('.JPEG')]
            for file in tqdm(files):
                futures.append(executor.submit(process_file, (source_dir, target_dir, subdir, file)))

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing files"):
            future.result()

if __name__ == "__main__":
    organize_imagenet()
    print("ImageNet organization complete.")
