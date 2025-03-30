import os
import yaml
from ultralytics import YOLO
import torch

# Get absolute path to current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to the script
yaml_path = os.path.join(current_dir, 'config/train_config.yaml')
results_dir = os.path.join(current_dir, 'runs', 'train')

# Load config to check structure (optional, but helps validate)
with open(yaml_path, 'r') as f:
    data_config = yaml.safe_load(f)

model_path = os.path.join(current_dir,'yolov8n.pt')

# Load model
model = YOLO(model_path)
print(f"🚀 Model is using device: {model.device}")

# Train
NAME = 'core_city'
num_epochs = 12
model.train(
    device=0,
    data=yaml_path,
    epochs=num_epochs,
    imgsz=640,
    batch=16,
    patience=12,
    project=results_dir,
    name= NAME + str(num_epochs),
    exist_ok=True
)

print(f"\n✅ Training complete. Results saved in: {os.path.join(results_dir, 'custom_yolov8')}")
