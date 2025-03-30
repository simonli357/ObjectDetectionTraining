import os
import cv2
import time
import argparse

import torch
import model.detector
import utils.utils
folder_path = "/home/slsecret/Downloads/bfmc_data/test_set/images"
weights = 'amy9sl'
if __name__ == '__main__':
    #指定训练配置文件
    print("hi~~~")
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='./data/coco.data', 
                        help='Specify training profile *.data')
    parser.add_argument('--weights', type=str, default='./weights/coco7sq.pth', 
                        help='The path of the .pth model to be transformed')
    parser.add_argument('--img', type=str, default='./car_test/sample2.jpg', 
                        help='The path of test image')

    opt = parser.parse_args()
    cfg = utils.utils.load_datafile(opt.data)
    assert os.path.exists(opt.weights), "请指定正确的模型路径"
    # assert os.path.exists(opt.img), "请指定正确的测试图像路径"

    #模型加载
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # device = torch.device("cpu")
    print("device is ", device)
    model = model.detector.Detector(cfg["classes"], cfg["anchor_num"], True).to(device)
    model.load_state_dict(torch.load('./weights/'+weights+'.pth', map_location=device))
    print("模型加载成功")
    #sets the module in eval node
    model.eval()
    i = 0
    os.makedirs("results_"+weights, exist_ok=True)
    # Loop through all the files in the folder
    print("start to test")
    for filename in os.listdir(folder_path):
        # Check if the file is an image
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".JPG"):
            i += 1
            #数据预处理
            t1 = time.time()
            ori_img = cv2.imread(os.path.join(folder_path, filename))
            # ori_img = cv2.imread(opt.img)
            res_img = cv2.resize(ori_img, (cfg["width"], cfg["height"]), interpolation = cv2.INTER_LINEAR) 
            img = res_img.reshape(1, cfg["height"], cfg["width"], 3)
            img = torch.from_numpy(img.transpose(0,3, 1, 2))
            img = img.to(device).float() / 255.0

            #模型推理
            # start = time.perf_counter()
            preds = model(img)
            # end = time.perf_counter()
            # time = (end - start) * 1000.
            # print("forward time:%fms"%time)

            #特征图后处理
            output = utils.utils.handel_preds(preds, cfg, device)
            output_boxes = utils.utils.non_max_suppression(output, conf_thres = 0.3, iou_thres = 0.4)

            #加载label names
            LABEL_NAMES = []
            with open(cfg["names"], 'r') as f:
                for line in f.readlines():
                    LABEL_NAMES.append(line.strip())
            
            h, w, _ = ori_img.shape
            scale_h, scale_w = h / cfg["height"], w / cfg["width"]

            #绘制预测框
            for box in output_boxes[0]:
                box = box.tolist()
            
                obj_score = box[4]
                category = LABEL_NAMES[int(box[5])]

                x1, y1 = int(box[0] * scale_w), int(box[1] * scale_h)
                x2, y2 = int(box[2] * scale_w), int(box[3] * scale_h)

                cv2.rectangle(ori_img, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.putText(ori_img, '%.2f' % obj_score, (x1, y1 - 5), 0, 0.7, (0, 255, 0), 2)	
                cv2.putText(ori_img, category, (x1, y1 - 25), 0, 0.7, (0, 255, 0), 2)
            print("time: ", time.time()-t1)
            # cv2.imshow("test_result.png", ori_img)
            # cv2.waitKey(2000)
            # cv2.destroyAllWindows()
            cv2.imwrite("results_"+weights+"/test_result"+str(i)+".png", ori_img)
    
    

