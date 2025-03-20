import os

# Set your folders
name = 'rf2024'
image_folder = f'/home/slsecret/Downloads/bfmc_data/images/{name}'
labels_folder = f'/home/slsecret/Downloads/bfmc_data/images/{name}_labels'

# Supported image formats
image_extensions = ('.jpg', '.jpeg', '.png')

# Count how many deleted
deleted_count = 0

for filename in os.listdir(image_folder):
    if filename.lower().endswith(image_extensions):
        base_name = os.path.splitext(filename)[0]
        label_file = os.path.join(labels_folder, base_name + '.txt')

        if not os.path.exists(label_file):
            image_path = os.path.join(image_folder, filename)
            os.remove(image_path)
            deleted_count += 1
            print(f"Deleted: {filename} (no label found)")

print(f"\n✅ Done! {deleted_count} unlabeled image(s) deleted.")
