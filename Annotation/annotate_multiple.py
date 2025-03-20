import cv2
import os

# Global variables
ix, iy = -1, -1
drawing = False
bounding_boxes = []
object_id = 0
filename = ''
zoom_level = 1.0
zoom_step = 0.1
min_zoom, max_zoom = 0.2, 5.0
pan_x, pan_y = 0, 0
cursor_x, cursor_y = 0, 0

# Class names and color map (BGR)
class_names = [
    "oneway", "highwayentrance", "stop", "roundabout", "parking",
    "crosswalk", "noentry", "highwayexit", "prio", "light",
    "block", "girl", "car"
]

class_colors = {
    0: (255, 0, 0),
    1: (0, 255, 0),
    2: (0, 0, 255),
    3: (255, 255, 0),
    4: (255, 0, 255),
    5: (0, 255, 255),
    6: (128, 0, 0),
    7: (0, 128, 0),
    8: (0, 0, 128),
    9: (128, 128, 0),
    10: (128, 0, 128),
    11: (0, 128, 128),
    12: (200, 200, 200),
}


def apply_zoom(img):
    h, w = img.shape[:2]
    new_w = int(w * zoom_level)
    new_h = int(h * zoom_level)
    zoomed_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    display_img = zoomed_img[
        pan_y:min(pan_y + h, zoomed_img.shape[0]),
        pan_x:min(pan_x + w, zoomed_img.shape[1])
    ]
    return display_img


def translate_coords(x, y):
    original_x = int((x + pan_x) / zoom_level)
    original_y = int((y + pan_y) / zoom_level)
    return original_x, original_y


def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, bounding_boxes, object_id, img
    global zoom_level, pan_x, pan_y, cursor_x, cursor_y

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = translate_coords(x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        cursor_x, cursor_y = x, y
        if drawing:
            x2, y2 = translate_coords(x, y)
            img_temp = img.copy()
            cv2.rectangle(img_temp, (ix, iy), (x2, y2), class_colors[object_id], 2)
            display = apply_zoom(img_temp)
            cv2.imshow(filename, display)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x2, y2 = translate_coords(x, y)
        bounding_boxes.append((object_id, ix, iy, x2 - ix, y2 - iy))
        cv2.rectangle(img, (ix, iy), (x2, y2), class_colors[object_id], 2)

    elif event == cv2.EVENT_MOUSEWHEEL:
        old_zoom = zoom_level
        direction = 1 if flags > 0 else -1
        if direction > 0:
            zoom_level = min(max_zoom, zoom_level + zoom_step)
        else:
            zoom_level = max(min_zoom, zoom_level - zoom_step)

        zoom_ratio = zoom_level / old_zoom
        pan_x = int((cursor_x + pan_x) * zoom_ratio - cursor_x)
        pan_y = int((cursor_y + pan_y) * zoom_ratio - cursor_y)

        pan_x = max(0, min(pan_x, int(img.shape[1] * zoom_level) - img.shape[1]))
        pan_y = max(0, min(pan_y, int(img.shape[0] * zoom_level) - img.shape[0]))

        print(f"Zoom level: {zoom_level:.2f}")


def save_annotation(filename, img_width, img_height, bounding_boxes):
    with open(filename, 'w') as f:
        for bbox in bounding_boxes:
            obj_id, x, y, width, height = bbox
            x_center = abs((x + width / 2) / img_width)
            y_center = abs((y + height / 2) / img_height)
            width = abs(width / img_width)
            height = abs(height / img_height)
            f.write(f"{obj_id} {x_center} {y_center} {width} {height}\n")


# Main loop
image_folder = '/home/slsecret/Downloads/bfmc_data/images/misc'
labels_folder = '/home/slsecret/Downloads/bfmc_data/images/misc_labels'
os.makedirs(labels_folder, exist_ok=True)

for file in os.listdir(image_folder):
    if file.endswith('.jpg') or file.endswith('.png'):
        img_path = os.path.join(image_folder, file)
        img = cv2.imread(img_path)
        img_height, img_width = img.shape[:2]

        txt_filename = os.path.splitext(file)[0] + '.txt'
        txt_path = os.path.join(labels_folder, txt_filename)
        filename = file

        if os.path.exists(txt_path):
            continue

        bounding_boxes = []
        zoom_level = 1.0
        pan_x, pan_y = 0, 0

        cv2.namedWindow(file)
        cv2.setMouseCallback(file, draw_rectangle)

        clean_img = img.copy()

        while True:
            img_temp = img.copy()

            # Live preview box while dragging
            if drawing:
                x2, y2 = translate_coords(cursor_x, cursor_y)
                cv2.rectangle(img_temp, (ix, iy), (x2, y2), class_colors[object_id], 2)
                cv2.putText(img_temp, class_names[object_id], (ix, iy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, class_colors[object_id], 1)

            # Redraw all existing boxes with class labels
            for box in bounding_boxes:
                obj_id, x, y, w, h = box
                cv2.rectangle(img_temp, (x, y), (x + w, y + h), class_colors[obj_id], 2)
                cv2.putText(img_temp, class_names[obj_id], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, class_colors[obj_id], 1)

            display = apply_zoom(img_temp)
            cv2.imshow(file, display)

            key = cv2.waitKey(1) & 0xFF

            # Object ID selection
            if ord('0') <= key <= ord('9'):
                object_id = int(chr(key))
                if object_id < len(class_names):
                    print(f"key is: {object_id}, class: {class_names[object_id]}")
            elif key == ord('i'):
                object_id = 10
                print(f"key is: {object_id}, class: {class_names[object_id]}")
            elif key == ord('o'):
                object_id = 11
                print(f"key is: {object_id}, class: {class_names[object_id]}")
            elif key == ord('p'):
                object_id = 12
                print(f"key is: {object_id}, class: {class_names[object_id]}")

            # Save
            elif key == ord('s'):
                save_annotation(txt_path, img_width, img_height, bounding_boxes)
                print("Saved annotation.")
                break

            # Pan using arrow keys
            elif key == 81:  # Left arrow
                pan_x = max(0, pan_x - 20)
            elif key == 82:  # Up arrow
                pan_y = max(0, pan_y - 20)
            elif key == 83:  # Right arrow
                pan_x = min(int(img.shape[1] * zoom_level) - img.shape[1], pan_x + 20)
            elif key == 84:  # Down arrow
                pan_y = min(int(img.shape[0] * zoom_level) - img.shape[0], pan_y + 20)

            # Undo
            elif key == ord('r'):
                if bounding_boxes:
                    bounding_boxes.pop()
                    img = clean_img.copy()
                    for box in bounding_boxes:
                        obj_id, x, y, w, h = box
                        cv2.rectangle(img, (x, y), (x + w, y + h), class_colors[obj_id], 2)
                    print("Removed last bounding box.")

            elif key == ord('q'):
                print("Skipped image.")
                break
            elif key == ord('x'):
                print("Exiting.")
                cv2.destroyAllWindows()
                exit()

        cv2.destroyAllWindows()
