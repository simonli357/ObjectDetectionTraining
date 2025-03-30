import os
import shutil
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

images_train = output_dir / 'images/train'
labels_train = output_dir / 'labels/train'

for p in [images_train, labels_train]:
    p.mkdir(parents=True, exist_ok=True)

# Helper to copy and avoid name collisions
def safe_copy(src_path, dst_dir, used_names, prefix=""):
    base = f"{prefix}_{src_path.stem}" if prefix else src_path.stem
    ext = src_path.suffix
    new_name = base
    i = 1
    while f"{new_name}{ext}" in used_names:
        new_name = f"{base}_{i}"
        i += 1
    used_names.add(f"{new_name}{ext}")
    dst_path = dst_dir / f"{new_name}{ext}"
    shutil.copy(src_path, dst_path)
    return new_name

used_image_names = set()

for folder_name in tqdm(datasets, desc="Combining datasets"):
    dataset_path = root_dir / folder_name
    image_dir = dataset_path / 'images'
    label_dir = dataset_path / 'labels'

    images = list(image_dir.glob('*.*'))
    for img_path in tqdm(images, desc=f"  Processing {folder_name}", leave=False):
        label_path = label_dir / (img_path.stem + '.txt')
        if label_path.exists():
            new_base = safe_copy(img_path, images_train, used_image_names, prefix=folder_name)
            label_dst_path = labels_train / f"{new_base}.txt"
            try:
                shutil.copy(label_path, label_dst_path)
            except Exception as e:
                print(f"❌ Failed to copy label for {img_path.name}: {e}")
                continue

print("✅ Dataset combination complete.")
