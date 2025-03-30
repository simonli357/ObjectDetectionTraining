import os
import shutil

# Root path
root = "/media/slsecret/E624108524105B3F/Users/simon/Downloads/linxy/cityscape/YOLOformat/processed_dataset"

# Source directories
image_src = os.path.join(root, "images/train")
label_src = os.path.join(root, "labels/train")

# Target directories
image_dst = os.path.join(root, "images2")
label_dst = os.path.join(root, "labels2")

# Create destination directories if they don't exist
os.makedirs(image_dst, exist_ok=True)
os.makedirs(label_dst, exist_ok=True)

# Start copying every 16th image and its label
i = 0
while True:
    image_name = f"{i}.png"
    label_name = f"{i}.txt"

    image_path = os.path.join(image_src, image_name)
    label_path = os.path.join(label_src, label_name)

    # Stop if the image doesn't exist
    if not os.path.exists(image_path):
        break

    # Copy image
    shutil.copy(image_path, os.path.join(image_dst, image_name))
    
    # Copy label if it exists
    if os.path.exists(label_path):
        shutil.copy(label_path, os.path.join(label_dst, label_name))

    i += 16

print("✅ Done copying every 16th image and label.")
