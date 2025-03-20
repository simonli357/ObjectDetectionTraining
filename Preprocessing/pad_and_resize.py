import cv2
import os
import numpy as np

# Input and output directories
input_dir = os.path.expanduser('~/Downloads/bfmc_data/images/team2021')
output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)

# Target aspect ratio and size
target_aspect_ratio = 640 / 480  # 4:3
target_width = 640
target_height = 480

# Supported image extensions
valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')

for filename in os.listdir(input_dir):
    if not filename.lower().endswith(valid_extensions):
        continue
    
    image_path = os.path.join(input_dir, filename)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Failed to read {filename}")
        continue

    h, w = image.shape[:2]
    current_aspect_ratio = w / h

    # Determine new size with padding to fit 4:3
    if current_aspect_ratio > target_aspect_ratio:
        # Image is too wide → pad top and bottom
        new_width = w
        new_height = int(w / target_aspect_ratio)
    else:
        # Image is too tall → pad left and right
        new_height = h
        new_width = int(h * target_aspect_ratio)

    # Calculate padding
    pad_top = (new_height - h) // 2
    pad_bottom = new_height - h - pad_top
    pad_left = (new_width - w) // 2
    pad_right = new_width - w - pad_left

    # Apply padding (black color)
    padded_image = cv2.copyMakeBorder(
        image, pad_top, pad_bottom, pad_left, pad_right,
        borderType=cv2.BORDER_CONSTANT, value=(0, 0, 0)
    )

    # Resize to final 640x480
    resized_image = cv2.resize(padded_image, (target_width, target_height), interpolation=cv2.INTER_AREA)

    # Save output
    output_path = os.path.join(output_dir, filename)
    cv2.imwrite(output_path, resized_image)
    print(f"Processed and saved: {filename}")

print("All images processed.")
