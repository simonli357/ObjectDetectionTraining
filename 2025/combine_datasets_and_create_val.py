import os
import shutil
import random
import yaml
from pathlib import Path
from tqdm import tqdm

# Load config
current_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_dir, 'config/datasets_config.yaml'), 'r') as f:
    config = yaml.safe_load(f)

root_dir = Path(config['root_dir'])
datasets = config['datasets']
output_dir = Path(config['output_dir'])
val_split = config.get('val_split', 0.1)

# Output structure
images_train = output_dir / 'images/train'
labels_train = output_dir / 'labels/train'
images_val = output_dir / 'images/val'
labels_val = output_dir / 'labels/val'

for p in [images_train, labels_train, images_val, labels_val]:
    p.mkdir(parents=True, exist_ok=True)

# Helper to copy and avoid name collisions
def safe_copy(src_path, dst_dir, used_names):
    base = src_path.stem
    ext = src_path.suffix
    new_name = base
    i = 1
    while f"{new_name}{ext}" in used_names:
        new_name = f"{base}_{i}"
        i += 1
    used_names.add(f"{new_name}{ext}")
    dst_path = dst_dir / f"{new_name}{ext}"
    shutil.copy(src_path, dst_path)
    return new_name  # return base name without extension

used_image_names = set()
all_image_label_pairs = []

# Process each dataset folder
for folder_name in tqdm(datasets, desc="Datasets"):
    dataset_path = root_dir / folder_name
    image_dir = dataset_path / 'images'
    label_dir = dataset_path / 'labels'

    images = list(image_dir.glob('*.*'))
    for img_path in tqdm(images, desc=f"  Processing {folder_name}", leave=False):
        label_path = label_dir / (img_path.stem + '.txt')
        if label_path.exists():
            new_base = safe_copy(img_path, images_train, used_image_names)
            try:
                shutil.copy(label_path, labels_train / f"{new_base}.txt")
                all_image_label_pairs.append((images_train / f"{new_base}{img_path.suffix}",
                                            labels_train / f"{new_base}.txt"))
            except Exception as e:
                print(f"❌ Failed to copy label {label_path} → {labels_train / f'{new_base}.txt'}: {e}")


# Shuffle and split for validation
random.shuffle(all_image_label_pairs)
val_count = int(len(all_image_label_pairs) * val_split)
val_pairs = all_image_label_pairs[:val_count]

for img_path, lbl_path in tqdm(val_pairs, desc="Splitting val set"):
    shutil.move(img_path, images_val / img_path.name)
    shutil.move(lbl_path, labels_val / lbl_path.name)

print(f"✅ Combined {len(all_image_label_pairs)} samples.")
print(f"🧪 Moved {val_count} samples to validation set.")
