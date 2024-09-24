import os
import glob
from tqdm import tqdm

def delete_zero_byte_npz_files(directory):
    zero_byte_count = 0
    total_count = 0
    
    # Use glob to find all .npz files in the specified directory and its subdirectories
    npz_files = glob.glob(os.path.join(directory, '**', '*.npz'), recursive=True)
    
    # Use tqdm to create a progress bar
    for npz_file in tqdm(npz_files, desc="Checking and deleting .npz files", unit="file"):
        total_count += 1
        if os.path.getsize(npz_file) == 0:
            zero_byte_count += 1
            os.remove(npz_file)
    
    return zero_byte_count, total_count

# Specify the directory to check
directory = '/workspace/cache'

# Delete zero-byte .npz files and count
deleted_files, total_files = delete_zero_byte_npz_files(directory)

print(f"Total .npz files: {total_files}")
print(f"Number of 0-byte .npz files deleted: {deleted_files}")
print(f"Percentage of deleted files: {(deleted_files / total_files) * 100:.2f}%")
