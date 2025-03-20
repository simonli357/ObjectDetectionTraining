import os
import random
import shutil

base_path = "C:/Users/simon/Downloads/linxy/YOLOv8/citydataset/cityscape_nosign"
train_image_folder = os.path.join(base_path, "images/train")
train_label_folder = os.path.join(base_path,  "labels/train")
val_image_folder = os.path.join(base_path, "images/val")
val_label_folder = os.path.join(base_path,  "labels/val")

# Create the validation folders if they don't exist
os.makedirs(val_image_folder, exist_ok=True)
os.makedirs(val_label_folder, exist_ok=True)

# Get the list of image files
image_files = [f for f in os.listdir(train_image_folder) if f.endswith(".png")]

# Calculate the number of images to move
num_images_to_move = int(len(image_files) * 0.05)

# Select random images to move
images_to_move = random.sample(image_files, num_images_to_move)

for image_file in images_to_move:
    # Move the image file
    shutil.move(os.path.join(train_image_folder, image_file),
                os.path.join(val_image_folder, image_file))

    # Move the corresponding label file
    label_file = os.path.splitext(image_file)[0] + ".txt"
    shutil.move(os.path.join(train_label_folder, label_file),
                os.path.join(val_label_folder, label_file))

print(f"Moved {num_images_to_move} images and labels to the validation folder.")
