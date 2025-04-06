import os
import shutil
from PIL import Image
import imagehash
from multiprocessing import Pool, cpu_count

# Set up folders
root = "/home/slsecret/Downloads/bfmc_data"
a_name = "rf2024c"
FOLDER_A = os.path.join(root, a_name)
FOLDER_B = os.path.join(root, "TestSetData/rf2024/images")
FOLDER_C = os.path.join(root, a_name + "_matched")

# Ensure output folder exists
os.makedirs(FOLDER_C, exist_ok=True)

# Resize target
RESIZE_TO = (320, 240)

# Load and hash all images in folder B
print("Hashing images in Folder B...")
hashes_b = set()

for filename in os.listdir(FOLDER_B):
    path = os.path.join(FOLDER_B, filename)
    try:
        with Image.open(path) as img:
            img = img.resize(RESIZE_TO).convert("L")
            img_hash = imagehash.average_hash(img)
            hashes_b.add(str(img_hash))
    except Exception as e:
        print(f"Error reading {path}: {e}")

print(f"Hashed {len(hashes_b)} images in Folder B.")

# Function for multiprocessing
def process_image_a(filename_a):
    path_a = os.path.join(FOLDER_A, filename_a)
    try:
        with Image.open(path_a) as img:
            img = img.resize(RESIZE_TO).convert("L")
            img_hash = imagehash.average_hash(img)
            if str(img_hash) in hashes_b:
                # Move the matching file to Folder C
                shutil.move(path_a, os.path.join(FOLDER_C, filename_a))
                return filename_a
    except Exception as e:
        print(f"Error processing {path_a}: {e}")
    return None

# Get list of images in A
images_a = os.listdir(FOLDER_A)

print(f"Processing {len(images_a)} images in Folder A using {cpu_count()} cores...")

# Parallel processing
with Pool(processes=cpu_count()) as pool:
    matches = pool.map(process_image_a, images_a)

# Report matches
matches = [m for m in matches if m]
print(f"✅ Found and moved {len(matches)} matching images to {FOLDER_C}")
