import os
import cv2
from concurrent.futures import ThreadPoolExecutor

try:
    base_path = os.path.dirname(os.path.abspath(__file__))
    print("base path is " + base_path)
except:
    # Fallback: If __file__ is not defined, use the current working directory
    base_path = os.getcwd()
    print("base path is " + base_path)
    
# Set the folder path containing the images to be resized
folder_path = "datasets/images/train"
label_path = "datasets/labels/train"
new_path = "datasets/images1/train"
new_label_path = "datasets/labels1/train"

# Set the new size for the images
new_size = (640, 640)
os.makedirs(os.path.join(base_path,new_path), exist_ok=True)

def resize_image(filename):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".JPG"):
        image = cv2.imread(os.path.join(folder_path, filename))
        # Resize the image
        resized_image = cv2.resize(image, new_size)
        with open(os.path.join(label_path, filename.split('.')[0]+'.txt'), "r") as f:
            # Read the contents of the file
            lines = f.readlines()
        new_lines = []
        for line in lines:
            # Remove the first space of the line
            line = line.split(" ")
            line[1] = str(float(line[1])*640/image.shape[1])
            line[2] = str(float(line[2])*640/image.shape[0])
            line[3] = str(float(line[3])*640/image.shape[1])
            line[4] = str(float(line[4])*640/image.shape[0])
            new_lines.append(' '.join(line))
        # Save the resized image with the same filename
        with open(os.path.join(new_label_path, filename.split('.')[0]+'.txt'), "w") as f:
                f.write("\n".join(new_lines) + "\n")
        cv2.imwrite(os.path.join(new_path, filename), resized_image)
        return 1
    return 0

# Loop through all the files in the folder using multithreading
with ThreadPoolExecutor() as executor:
    results = list(executor.map(resize_image, os.listdir(folder_path)))

print(f"Processed {sum(results)} images")

