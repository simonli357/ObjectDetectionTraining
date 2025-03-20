# Extract frames from video file and save them as images
import cv2
import os

def save_frames(video_path, output_folder, fps=5, name="trackA"):
    video = cv2.VideoCapture(video_path)
    video_fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_interval = video_fps // fps

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    saved_count = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            output_filename = os.path.join(output_folder, f"{name}_{saved_count+311:04d}.jpg")
            cv2.imwrite(output_filename, frame)
            saved_count += 1

        frame_count += 1

    video.release()


video_path = "/home/slsecret/Downloads/bfmc_data/videos/testvid.mp4"
output_folder = "/home/slsecret/ObjectDetectionTraining/basement2"

save_frames(video_path, output_folder, fps=5, name = "testvid")
