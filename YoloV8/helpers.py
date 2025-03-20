import os
import cv2
import shutil
import random
import numpy as np
import pandas as pd

# filter out the things in labels that are too small or too unproportional
# labelpath = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset/train/labels/"
# newlabelpath = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset/labels/val/"
# dirs = os.listdir(newlabelpath)
# # read label
# for dir in dirs:
#     if not dir.startswith("city"):
#         continue
#     with open(newlabelpath + dir,"r") as f:
#         lines = f.readlines()
    ## filter out car that are too small or too unproportional
    
    # new_label = ""
    # for line in lines:
    #     if line.startswith("/n"):
    #         continue
    #     line = line.split(" ")
        # if line[0] == "":
        #     continue
        # line[0] = str(int(float(line[0])))
        # if line[0] == "9":
            # if (float(line[3])/float(line[4]) > 2 or float(line[4])/float(line[3]) > 2) and (float(line[3])*640<30 or float(line[4])*320<30):
            #     continue
            # elif (float(line[3])/float(line[4]) > 5):
            #     continue
            # elif (float(line[3])/float(line[4]) > 4) and (float(line[3]) > 0.7):
            #     continue
                
            # elif float(line[3])*640<40 and float(line[4])*320<30:
            #     continue
        # for i in range(1,5):
        #     line[i] = str(abs(float(line[i])))
        # else:
        #     continue
    # with open(newlabelpath + dir,"w") as f:
    #         f.write(new_label)


# # remove coco val label
# labelpath = "citydataset/past6/images/val/"
# dirs = os.listdir(labelpath)
# # read label
# for dir in dirs:
#     if not dir.startswith("000000"):
#         continue
#     os.remove(labelpath + dir)
#     # os.remove("citydataset/images/val/" + dir[:-4] + ".png")
#     # shutil.copyfile("citydataset/coco/labels/train/" + dir, labelpath + dir)

# # resize images for training
# labelpath = "citydataset/girl&light/labels/"
# imagepath = "citydataset/girl&light/images/"
# dirs = os.listdir(labelpath)
# for dir in dirs:
#     if os.path.exists(imagepath + dir[:-4] + ".jpg"):
#         with open(labelpath + dir,"r") as f:
#             lines = f.readlines()
#         img = cv2.imread(imagepath + dir[:-4] + ".jpg")
#         h,w,_ = img.shape
#         new_label = ""  
#         for line in lines:
#             line = line.split(" ")
#             line[0] = str(int(float(line[0])))
#             line[1] = str(float(line[1]))
#             line[2] = str(float(line[2]))
#             line[3] = str(float(line[3]))
#             line[4] = str(float(line[4]))
#             new_label += " ".join(line)
#         # img = cv2.resize(img,(640,640))
#         # cv2.imwrite(imagepath + "lg" +dir[:-4] + ".png",img)
#         with open(labelpath + "lg" + dir,"w") as f:
#             f.write(new_label)

# # rename files
# path = "citydataset/track_training/track_images//"
# newpath = "citydataset/track_training/track_images//"
# labelpath = "citydataset/track_training/track_labels//"
# # labelpath = "YOLOformat/yolo dataset/train_coco128/labels/"
# dirs = os.listdir(path)
# count = 0
# for dir in dirs:
#     if os.path.exists(path + str(dir) ):
#         os.rename(path + str(dir), newpath + "track" + str(count) + ".png")
#         os.rename(labelpath + dir[:-4] + ".txt", labelpath + "track" + str(count) + ".txt")
#         count += 1

# move sign photo of iphone to training dataset
# origin = "C:/Users/simon/Downloads/linxy/signs/iphone_sign"
# originlabel = "C:/Users/simon/Downloads/linxy/signs/iphone_labels"
# destination = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset/images/train"
# destlabel = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset/labels/train"
# random = random.sample(range(0,100),5)
# files = os.listdir(originlabel)
# for i in range(len(files)):
#     file = files[i]
#     if i not in random:
#         # if file.endswith(".jpg"):
#         shutil.copy(origin + "/" + file[:-4] + ".JPG", destination + "/" + "ic" + file[:-4] + ".jpg")
#         shutil.copy(originlabel + "/" + file, destlabel + "/" + "ic" + file[:-4] + ".txt")
#     else:
#         # if file.endswith(".jpg"):
#         shutil.copy(origin + "/" + file[:-4] + ".JPG", destination[:-5] + "val" + "/" + "ic" + file[:-4] + ".jpg")
#         shutil.copy(originlabel + "/" + file, destlabel[:-5] + "val" + "/" + "ic" + file)

# # remove some imgs of cityscape from training dataset
# destination = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset/images/train"
# destlabel = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset/labels/train"
# random = random.sample(range(0,45038-1),10000)
# labelist = os.listdir(destlabel)
# for i in random:
#         # label = labelist[i]
#         if os.path.exists(destlabel + "/city" + str(i) + ".txt"):
#             os.remove(destlabel + "/city" + str(i) + ".txt")
#             os.remove(destination + "/city" + str(i) + ".png")

# destination = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset/images/train"
# destlabel = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset/labels/train"
# for img in os.listdir(destination):
#     # png = os.path.exists(destination + "/" + label[:-4] + ".png")
#     # jpg = os.path.exists(destination + "/" + label[:-4] + ".jpg")
#     if not (os.path.exists(destlabel + "/" + img[:-4] + ".txt")):
#         # os.remove(destlabel + "/" + label)
#         # if png:
#         os.remove(destination + "/" + img)
#         # elif jpg:
#         #     os.remove(destination + "/" + label[:-4] + ".jpg")

# folder = "C:/Users/simon/Downloads/Yolo-FastestV2/datasets/val"
# newimgfolder = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset_yolov2/images/val"
# newlabelfolder = "C:/Users/simon/Downloads/linxy/YOLOv8/dataset_yolov2/labels/val"
# os.makedirs(newimgfolder,exist_ok=True)
# os.makedirs(newlabelfolder,exist_ok=True)
# count = 0
# for file in os.listdir(folder):
#     if file.endswith(".txt"):
#         shutil.copy(folder + "/" + file, newlabelfolder + "/" + file)
#     else:
#         shutil.copy(folder + "/" + file, newimgfolder + "/" + file)
#     count += 1
#     if count%1000 == 0:
#         print(count)

# v8imgPath = "c:/Users/simon/Downloads/linxy/YOLOv8/datasets_else/everything/images/val/"
# v8labelPath = "c:/Users/simon/Downloads/linxy/YOLOv8/datasets_else/everything/labels/val/"
# v2imgPath = "c:/Users/simon/Downloads/linxy/YOLOv8/datasets_else/yolov2_1/images/val/"
# v2labelPath = "c:/Users/simon/Downloads/linxy/YOLOv8/datasets_else/yolov2_1/labels/val/"
# os.makedirs(v2imgPath,exist_ok=True)
# os.makedirs(v2labelPath,exist_ok=True)
# for file in os.listdir(v8imgPath):
#     if file.endswith(".jpg") and file[0].isdigit():
#         shutil.move(v8imgPath+file,v2imgPath+file)
#         shutil.move(v8labelPath+file[:-4]+".txt",v2labelPath+file[:-4]+".txt")

# v8imgPath = "dataset/images/train/"
# v8labelpath = "dataset/labels/train/"
# # # filenames = "C:/Users/simon/Downloads/linxy/YOLOv8/citydataset/cityscape_nosign/images/train/"
# # # originImgPath = "c:/Users/simon/Downloads/ObjectDection/Preprocessing/datasets/coco128/images/train/"
# # # originLabelPath = "c:/Users/simon/Downloads/ObjectDection/Preprocessing/datasets/coco128/labels/train/"
# destImgPath = "dataset/v2 removed from train/images/train/"
# destLabelPath = "dataset/v2 removed from train/labels/train/"
# os.makedirs(destImgPath,exist_ok=True)
# os.makedirs(destLabelPath,exist_ok=True)
# series = pd.DataFrame(os.listdir(v8imgPath),columns=["filename"])["filename"]
# filelist = series.str.contains("else4")
# # print(filelist)
# fileindexes = filelist[filelist==True].index
# # print(fileindexes)
# randindexes = random.sample(range(1,len(fileindexes)),k=200)
# for index in randindexes:
#     # print(index)
#     file = series[fileindexes[index]]
#     # print(file)
#     shutil.move(v8imgPath+file,destImgPath+file)
#     shutil.move(v8labelpath+file[:-4]+".txt",destLabelPath+file[:-4]+".txt")
# # for file in os.listdir(destLabelPath):
#     shutil.move(destLabelPath+file,v8labelpath+file)
#     shutil.move(destImgPath+file[:-4]+".png",v8imgPath+file[:-4]+".png")


# newImgPath = "datasets_else/track2024/images/"
# newLabelPath = "datasets_else/track2024/labels/"
# oldImgPath = "/media/slsecret/E624108524105B3F/Users/simon/Downloads/ObjectDection/Annotation/track_images/"
# oldLabelPath = "/media/slsecret/E624108524105B3F/Users/simon/Downloads/ObjectDection/Annotation/track_labels/"
# i = len(os.listdir(newLabelPath))
# for file in os.listdir(oldLabelPath):
#     if file[:-4] in ([img[:-4] for img in os.listdir(oldImgPath)]):
#         shutil.move(oldLabelPath+file,newLabelPath+"track"+str(i)+".txt")
#         shutil.move(oldImgPath+file[:-4]+".jpg",newImgPath+"track"+str(i)+".jpg")
#         i+=1
# i=0
# for file in os.listdir(newImgPath):
#     os.rename(newImgPath+file,newImgPath+"track"+str(i)+".jpg")
#     os.rename(newLabelPath+file[:-4]+".txt",newLabelPath+"track"+str(i)+".txt")
#     i+=1

# newImgPath = "dataset/images//"
# newlabelPath = "dataset/labels/"
# oldImgPath = "C:/Users/simon/Downloads/ObjectDection/Preprocessing/datasets/coco128/images/train/"
# oldLabelPath = "C:/Users/simon/Downloads/ObjectDection/Preprocessing/datasets/coco128/labels/train/"
# # oldImgPath = "C:/Users/simon/Downloads/ObjectDection/Preprocessing/datasets/coco128/images/train/"
# # # oldlabelPath = "C:/Users/simon/Downloads/ObjectDection/Preprocessing/datasets/coco128/labels/train/"  


# counter = 1
# # listfile = os.listdir(oldlabelPath)
# # for file in os.listdir(oldImgPath):
# #     if file[:-4]+".txt" not in os.listdir("dataset/labels/val/"):
# #         shutil.copy(oldImgPath+file,newImgPath+file)
# #         shutil.copy(oldLabelPath+file[:-4]+".txt",newlabelPath+file[:-4]+".txt")
# #         shutil.copy(oldImgPath+file,toimgPath+file)
# #         shutil.copy(oldLabelPath+file[:-4]+".txt",tolabelPath+file[:-4]+".txt")
# #         counter += 1
# #         if counter%1000 == 0:
# #             print(counter)
# filelist = os.listdir(oldImgPath)
# total = len(filelist)
# for file in filelist:
#     if int(file[:-4]) < total*0.95:
#         shutil.move(oldImgPath+file,newImgPath+"train/"+"else" + file)
#         shutil.move(oldLabelPath+file[:-4]+".txt",newlabelPath+"train/"+"else"+file[:-4]+".txt") 
#     else:
#         shutil.move(oldImgPath+file,newImgPath+"val/"+"else"+file)
#         shutil.move(oldLabelPath+file[:-4]+".txt",newlabelPath+"val/"+"else"+file[:-4]+".txt")
    
#     counter += 1
#     if counter%1000 == 0:
#         print(counter)


# # correct labels in track annotation
# newImgPath = "dataset/images/"
# newlabelPath = "dataset/labels/train/"

# for file in os.listdir(newlabelPath):
#     if file.startswith("track"):
#         with open(newlabelPath+file,"r") as f:
#             lines = f.readlines()
#         new_label = ""
#         for line in lines:
#             line = line.split(" ")
#             if len(line) == 5:
#                 if line[0] == "1":
#                     line[0] = "7"
#                 elif line[0] == "7":
#                     line[0] = "1"
#                 new_label += " ".join(line)
#             else:
#                 print(file)
#         with open(newlabelPath+file,"w") as f:
#             f.write(new_label)

# rename and create labels for empty backgrounds
labelPath = "datasets_else/background/labels/"
bgPath = "datasets_else/background/images/"
newlabelPath = "dataset/labels/train/"
newimgPath = "dataset/images/train/"

trainVal = 0.8

filelist = os.listdir(bgPath)
for i in range (len(filelist)):
    os.rename(bgPath+filelist[i],bgPath+"emptybg"+str(i)+".jpg")
    with open(labelPath+"emptybg"+str(i)+".txt","w") as f:
        f.write("")
    if i < len(filelist)*trainVal:
        shutil.copy(bgPath+"emptybg"+str(i)+".jpg",newimgPath+"emptybg"+str(i)+".jpg")
        shutil.copy(labelPath+"emptybg"+str(i)+".txt",newlabelPath+"emptybg"+str(i)+".txt")
    else:
        shutil.copy(bgPath+"emptybg"+str(i)+".jpg","dataset/images/val/emptybg"+str(i)+".jpg")
        shutil.copy(labelPath+"emptybg"+str(i)+".txt","dataset/labels/val/emptybg"+str(i)+".txt")