#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <n>"
    echo "Where <n> is the number of the tar file to extract (0-4)"
    exit 1
fi

# Get the argument
n=$1

# Define source and target directories
SOURCE_DIR="/workspace/imagenet-1k/data/"
TARGET_DIR="/workspace/imagenet-1k/data/train/"

# Function to extract a single tar file using pigz
extract_tar() {
    local n=$1
    local tar_file="train_images_${n}.tar.gz"
    local tar_path="${SOURCE_DIR}${tar_file}"
    local extract_path="${TARGET_DIR}${n}"

    if [ -f "$tar_path" ]; then
        echo "Extracting ${tar_file}..."
        mkdir -p "$extract_path"
        pv "$tar_path" | tar -xzf - -C "$extract_path" --no-same-owner
        echo "Extraction of ${tar_file} completed."
    else
        echo "Warning: ${tar_file} not found in ${SOURCE_DIR}"
    fi
}

# Main execution
echo "Starting extraction process for tar file $n..."

# Extract the specified file
extract_tar $n

echo "Extraction completed for tar file $n."
