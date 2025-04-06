import os

# Set your paths
IMAGE_FOLDER = "/home/slsecret/Downloads/bfmc_data/TestSetData/car_test_padded"
LABEL_FOLDER = "/home/slsecret/Downloads/bfmc_data/TestSetData/car_test_padded_labels"

# Accepted image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# Get base filenames without extensions
def get_file_basenames(folder, extensions):
    return {
        os.path.splitext(f)[0]
        for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in extensions
    }

def main():
    image_names = get_file_basenames(IMAGE_FOLDER, IMAGE_EXTENSIONS)
    label_names = get_file_basenames(LABEL_FOLDER, {'.txt'})

    missing_labels = image_names - label_names
    missing_images = label_names - image_names

    if missing_labels:
        print("🟥 Images without labels:")
        for name in sorted(missing_labels):
            print(f"  {name}")
    else:
        print("✅ All images have labels.")

    if missing_images:
        print("\n🟨 Labels without images:")
        for name in sorted(missing_images):
            print(f"  {name}")
    else:
        print("✅ All labels have matching images.")

if __name__ == "__main__":
    main()
