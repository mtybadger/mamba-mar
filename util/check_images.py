import os
from PIL import Image
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def check_image(file_path):
    """
    Check if an image file is valid.

    Args:
    file_path (str): Path to the image file.

    Returns:
    tuple: (file_path, is_valid, error_message)
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return file_path, True, None
    except Exception as e:
        return file_path, False, str(e)

def check_image_folder(folder_path):
    """
    Check a folder for valid/invalid JPEG images using PIL.

    Args:
    folder_path (str): Path to the folder containing images.

    Returns:
    tuple: (valid_count, invalid_count, invalid_files)
    """
    valid_count = 0
    invalid_count = 0
    invalid_files = []

    for filename in os.listdir(folder_path), desc=f"Checking {os.path.basename(folder_path)}":
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            _, is_valid, error = check_image(file_path)
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                invalid_files.append((file_path, error))

    return valid_count, invalid_count, invalid_files

def check_all_train_folders(train_path):
    """
    Check all folders under the train directory for valid/invalid images.

    Args:
    train_path (str): Path to the train directory.

    Returns:
    dict: A dictionary with folder names as keys and (valid_count, invalid_count, invalid_files) as values.
    """
    results = {}
    total_valid = 0
    total_invalid = 0

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info(f"Starting to check all folders under {train_path}")

    folders = [f for f in os.listdir(train_path) if os.path.isdir(os.path.join(train_path, f))]
    with ProcessPoolExecutor() as executor:
        future_to_folder = {executor.submit(check_image_folder, os.path.join(train_path, folder)): folder for folder in folders}
        
        for future in tqdm(as_completed(future_to_folder), total=len(folders), desc="Checking folders"):
            folder_name = future_to_folder[future]
            try:
                valid_count, invalid_count, invalid_files = future.result()
                results[folder_name] = (valid_count, invalid_count, invalid_files)
                total_valid += valid_count
                total_invalid += invalid_count
                logger.info(f"Folder {folder_name}: Valid: {valid_count}, Invalid: {invalid_count}")
                if invalid_files:
                    logger.warning(f"Invalid files in {folder_name}:")
                    for file, error in invalid_files:
                        logger.warning(f"  {file}: {error}")
            except Exception as exc:
                logger.error(f"{folder_name} generated an exception: {exc}")

    logger.info(f"Finished checking all folders")
    logger.info(f"Total valid images: {total_valid}")
    logger.info(f"Total invalid images: {total_invalid}")

    return results

if __name__ == "__main__":
    train_path = "/workspace/imagenet-1k/train"
    results = check_all_train_folders(train_path)

    print("\nSummary:")
    for folder, (valid, invalid, _) in results.items():
        print(f"{folder}: Valid: {valid}, Invalid: {invalid}")

