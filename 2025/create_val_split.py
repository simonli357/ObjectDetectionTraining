import os
import shutil
import yaml
from pathlib import Path
from tqdm import tqdm

# Load config
current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, 'config/datasets_config.yaml'), 'r') as f:
    config = yaml.safe_load(f)

output_dir = Path(config['output_dir'])
val_split = config.get('val_split', 0.1)

images_train = output_dir / 'images/train'
labels_train = output_dir / 'labels/train'
images_val = output_dir / 'images/val'
labels_val = output_dir / 'labels/val'

for p in [images_val, labels_val]:
    p.mkdir(parents=True, exist_ok=True)

# Gather all image-label pairs
image_files = sorted(images_train.glob('*.*'))  # sorted for determinism
all_pairs = []

for img_path in image_files:
    label_path = labels_train / (img_path.stem + '.txt')
    if label_path.exists():
        all_pairs.append((img_path, label_path))

# Deterministic val split: take every Nth sample
step = int(1 / val_split)
val_pairs = all_pairs[::step]

for img_path, lbl_path in tqdm(val_pairs, desc="Creating val split"):
    if not img_path.exists() or not lbl_path.exists():
        print(f"⚠️ Missing file: {img_path}, {lbl_path}")
        continue
    shutil.move(img_path, images_val / img_path.name)
    shutil.move(lbl_path, labels_val / lbl_path.name)

print(f"✅ Moved {len(val_pairs)} samples to validation set (every {step}th item).")
