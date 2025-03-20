import os
import shutil

folder_path = 'C:/Users/simon/Downloads/linxy/YOLOv8/dataset_yolov2/train'
# os.chdir(folder_path)
# os.mkdir('labels')
# for filename in os.listdir(folder_path):

#     # Move the file to the destination directory
#     shutil.move(filename, "labels")

# os.mkdir("images")
# source_path = 'C:/Users/simon/Downloads/Yolo-FastestV2/datasets_t/train640'
# counter = 0
# for filename in os.listdir(source_path):
#     if filename.endswith('.jpg'):
#         shutil.copy(os.path.join(source_path, filename), folder_path+'/images')
#     counter += 1
#     if counter%1000==0:
#         print(counter)


# os.mkdir("C:/Users/simon/Downloads/linxy/YOLOv8/dataset_yolov2/val/images")
for filename in os.listdir(folder_path+'/labels'):
    if filename[:-4]+'.jpg' not in os.listdir(folder_path+'/images'):
        print(filename[:-4]+'.jpg'+' not in images')
        # os.remove(folder_path+'/labels/'+filename)
        # shutil.move(folder_path+'/images/'+filename,'C:/Users/simon/Downloads/linxy/YOLOv8/dataset_yolov2/val/images')
        