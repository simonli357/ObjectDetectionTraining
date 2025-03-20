from ultralytics import YOLO

# model = YOLO('yolov8n.pt')  # initialize
# results = model.train(data="custom_coco.yaml",epochs=5)  # train
# model.export(format="onnx",single_precision=False)  # export
# model.save("yolov8n.pt")  # save

model = YOLO('yolov8n.pt')  # initialize
if __name__ == '__main__':
    model.train(data="custom_coco.yaml",epochs=24,save_period=2,batch=12,workers=6)  # traib
# model.export(format="engine")  # export
# model.save("yolov8n.pt")  # save
# model = YOLO('yolov8n.pt')
# model.train(data="custom_coco.yaml",epochs=50,batch=12,workers=6)

    # yolo val model=runs/detect/train/weights/best.pt data=custom_coco.yaml batch=1 imgsz=640
    # yolo predict model=runs/detect/train20/weights/best.pt source=C:/Users/simon/Downloads/yolov5/car_test
    # yolo predict model=runs/detect/train25/weights/best.pt source=c:/Users/simon/Downloads/linxy/YOLOv8/2024qualiRun.mp4
    # yolo predict model=runs/detect/train2weights/best.pt source=C:/Users/simon/Downloads/ObjectDection/Annotation/track_images
    # yolo predict model=runs/detect/citycocov2lgtclab_20/weights/citycocov2lgtclab_20weights.pt source=c:/Users/simon/Downloads/linxy/YOLOv8/testSet