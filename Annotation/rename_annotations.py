import os

base_dir = "/home/slsecret/Downloads/bfmc_data/images/"
name = "car_test_padded"
img_folder = os.path.join(base_dir, name + "/")
label_folder = os.path.join(base_dir, name + "_labels/")

# List and sort all .jpg files in the image folder
img_files = sorted([f for f in os.listdir(img_folder) if f.lower().endswith(".jpg") or f.lower().endswith(".jpeg") or f.lower().endswith(".png")])

# Process each image and its corresponding label
for i, img_file in enumerate(img_files):
    # Create the new file name using the folder name + index
    new_img_name = f"{name}{i}.jpg"  # e.g. car_test_padded0.jpg
    old_img_path = os.path.join(img_folder, img_file)
    new_img_path = os.path.join(img_folder, new_img_name)
    
    # Rename the image file
    os.rename(old_img_path, new_img_path)
    print(f"Renamed image: {img_file} -> {new_img_name}")

    # Prepare for the corresponding label file:
    # Assumes the label file has the same base name with a .txt extension
    base_name = os.path.splitext(img_file)[0]
    label_file = base_name + ".txt"
    old_label_path = os.path.join(label_folder, label_file)
    
    new_label_name = f"{name}{i}.txt"  # e.g. car_test_padded0.txt
    new_label_path = os.path.join(label_folder, new_label_name)
    
    # Rename the label file if it exists
    if os.path.exists(old_label_path):
        os.rename(old_label_path, new_label_path)
        print(f"Renamed label: {label_file} -> {new_label_name}")
    else:
        print(f"Warning: Label file {old_label_path} does not exist.")
