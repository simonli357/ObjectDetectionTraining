from ultralytics import YOLO
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
MODEL = "core_city12"
model_path = os.path.join(current_dir, "models/"+MODEL+".pt")

yaml_path = os.path.join(current_dir, "config/train_config.yaml")

model = YOLO(model_path)

#get real mAP
metrics = model.val(device=0, data=yaml_path, split='test', save_dir=os.path.join(current_dir, "results"))

#save results
# output_dir = os.path.join(current_dir, "results/" + MODEL)
# metrics = model.val(
#     device=0
#     data=yaml_path,
#     split='test',
#     save=True,               # Save images with predictions
#     save_txt=True,           # Save predictions to .txt files
#     save_conf=True,          # Save confidences in txt
#     save_hybrid=True,        # Save hybrid format (xywh + class + conf)
#     project=output_dir,      # Ensures output goes to your "results" folder
#     name='test_results',     # So it's saved under results/test_results
#     exist_ok=True            # Overwrite if folder already exists
# )