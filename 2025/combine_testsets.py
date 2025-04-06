import os
import shutil
import yaml

def load_yaml_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def combine_datasets(config_path):
    config = load_yaml_config(config_path)

    output_name = config.get('output_name')
    output_base_dir = config.get('output_base_dir')
    datasets = config.get('datasets', [])

    if not output_name or not output_base_dir or not datasets:
        print("[ERROR] Missing required keys in config: 'output_name', 'output_base_dir', or 'datasets'")
        return

    output_image_dir = os.path.join(output_base_dir, output_name, "images")
    output_label_dir = os.path.join(output_base_dir, output_name, "labels")

    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    total_images = 0
    for dataset in datasets:
        img_dir = os.path.join(output_base_dir, dataset, "images")
        label_dir = os.path.join(output_base_dir, dataset, "labels")

        if not os.path.isdir(img_dir) or not os.path.isdir(label_dir):
            print(f"[WARNING] Skipping {dataset} - missing image or label directory.")
            continue

        for img_file in os.listdir(img_dir):
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            base_name, ext = os.path.splitext(img_file)
            label_file = base_name + ".txt"

            img_path = os.path.join(img_dir, img_file)
            label_path = os.path.join(label_dir, label_file)

            if not os.path.exists(label_path):
                print(f"[WARNING] Missing label for {img_file} in {dataset}")
                continue

            # Avoid collisions by prefixing with dataset name
            new_base = f"{dataset}_{base_name}"
            new_img_name = new_base + ext
            new_label_name = new_base + ".txt"

            shutil.copyfile(img_path, os.path.join(output_image_dir, new_img_name))
            shutil.copyfile(label_path, os.path.join(output_label_dir, new_label_name))

            total_images += 1

    print(f"\n✅ Done! Combined {total_images} images into:")
    print(f"   Images: {output_image_dir}")
    print(f"   Labels: {output_label_dir}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config/test_config.yaml")
    combine_datasets(config_path)
