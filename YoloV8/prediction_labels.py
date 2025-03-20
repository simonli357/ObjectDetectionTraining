import os
from ultralytics import YOLO

model = YOLO('model_city/best3_cococityyololg40/train7/weights/best.pt')

def predict(image_path):
    predictions = model(image_path)

    with open(os.path.join(pred_labels_path,image_path[:-4]+".txt"), 'w') as file:
        for idx, prediction in enumerate(predictions[0].boxes.xywhn): # change final attribute to desired box format
            cls = int(predictions[0].boxes.cls[idx].item())
            # Write line to file in YOLO label format : cls x y w h
            file.write(f"{cls} {prediction[0].item()} {prediction[1].item()} {prediction[2].item()} {prediction[3].item()}\n")

source_path = "C:/Users/simon/Downloads/linxy/cityscape/YOLOformat/yolo sign blurred/images/train"
pred_labels_path = "C:/Users/simon/Downloads/linxy/cityscape/YOLOformat/yolo sign blurred/pred_labels/train"
os.makedirs(pred_labels_path, exist_ok=True)
for filename in os.listdir(source_path):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        predict(os.path.join(source_path, filename))
    else:
        continue
    print(f"Predicted labels for {filename} saved to {pred_labels_path}")
