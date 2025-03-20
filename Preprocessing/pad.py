import os
import random
import cv2
import numpy as np
import shutil
from concurrent.futures import ThreadPoolExecutor
import time

# Set the base path to the image and label folders
base_path = "C:/Users/simon/Downloads/datacar"

# Create new folders if they don't exist
os.makedirs(os.path.join(base_path, "images_pad2"), exist_ok=True)
os.makedirs(os.path.join(base_path, "labels_pad2"), exist_ok=True)

n = 30955  # number of images
target_width = 853
target_height = 640  # Add target_height

def process_image(idx):
    # Prepare paths
    original_image_path = (base_path + "/images_square/" + f"{idx}.jpg")
    original_label_path = (base_path + "/labels_square/" + f"{idx}.txt")
    new_image_path = (base_path + "/images_pad2/" + f"{idx}.jpg")
    new_label_path = (base_path + "/labels_pad2/" + f"{idx}.txt")

    # Read image and label
    img = cv2.imread(original_image_path)
    if img is None:
        print(f"Could not read image {original_image_path}")
        return 0

    img_height, img_width, _ = img.shape

    with open(original_label_path, "r") as label_file:
        label = label_file.readline().strip().split()
        class_id, x_center, y_center, width, height = [float(x) for x in label]

    # Calculate the padding needed to make the image have a width of target_width and height of target_height
    padding_width = target_width - img_width
    pad_left = random.randint(0, padding_width)
    pad_right = padding_width - pad_left

    padding_height = target_height - img_height
    pad_top = random.randint(0, padding_height)
    pad_bottom = padding_height - pad_top

    # Generate a random RGB color for padding
    random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Pad the image
    img_padded = cv2.copyMakeBorder(img, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=random_color)

    # Update label to account for the padding
    new_x_center = (x_center * img_width + pad_left) / target_width
    new_width = width * img_width / target_width
    new_y_center = (y_center * img_height + pad_top) / target_height
    new_height = height * img_height / target_height

    # Write the new label file
    with open(new_label_path, "w") as new_label_file:
        new_label_file.write(f"{int(class_id)} {new_x_center} {new_y_center} {new_width} {new_height}\n")

    # Save the new padded image
    cv2.imwrite(new_image_path, img_padded)
    return 1

t1 = time.time()
# Use ThreadPoolExecutor for multithreading
with ThreadPoolExecutor() as executor:
    results = list(executor.map(process_image, range(n)))

print(f"Processed {sum(results)} images")
print("time: ", time.time()-t1)
