import cv2
import os

# ----------------- Configuration ------------------
IMAGE_FOLDER = "/home/slsecret/Downloads/bfmc_data/images/xinya"
LABEL_FOLDER = "/home/slsecret/Downloads/bfmc_data/images/xinya_labels"
os.makedirs(LABEL_FOLDER, exist_ok=True)

CLASS_NAMES = [
    "oneway", "highwayentrance", "stop", "roundabout", "parking",
    "crosswalk", "noentry", "highwayexit", "prio", "light",
    "block", "girl", "car"
]
CLASS_COLORS = [
    (0, 255, 0),     # oneway - green
    (255, 0, 0),     # highwayentrance - blue
    (0, 0, 255),     # stop - red
    (255, 255, 0),   # roundabout - cyan
    (255, 0, 255),   # parking - magenta
    (0, 255, 255),   # crosswalk - yellow
    (128, 0, 128),   # noentry - purple
    (0, 128, 255),   # highwayexit - orange
    (128, 128, 0),   # prio - olive
    (0, 128, 128),   # light - teal
    (128, 0, 0),     # block - maroon
    (0, 0, 128),     # girl - navy
    (128, 128, 128)  # car - gray
]

CLASS_KEYS = {str(i): i for i in range(10)}
CLASS_KEYS.update({"i": 10, "o": 11, "p": 12})

# ----------------- State Variables ------------------
boxes = []
selected_box = None
dragging = False
adding_box = False
new_box_start = None
new_box_current = None
start_x = start_y = 0
pan_x = pan_y = 0
zoom = 1.0
zoom_step = 0.1
min_zoom = 0.5
max_zoom = 5.0
cursor_x = cursor_y = 0
current_image_index = 0
image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.endswith((".jpg", ".png"))])

# ----------------- BoundingBox Class ------------------
class BoundingBox:
    def __init__(self, class_id, x, y, w, h):
        self.class_id = class_id
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.selected = False
        self.handle_selected = None

    def get_rect(self):
        return self.x, self.y, self.x + self.w, self.y + self.h

    def get_center(self):
        return self.x + self.w // 2, self.y + self.h // 2

    def get_handles(self):
        x1, y1, x2, y2 = self.get_rect()
        return {
            'tl': (x1, y1), 'tr': (x2, y1), 'bl': (x1, y2), 'br': (x2, y2),
            'l': (x1, y1 + self.h // 2), 'r': (x2, y1 + self.h // 2),
            't': (x1 + self.w // 2, y1), 'b': (x1 + self.w // 2, y2)
        }

    def draw(self, img):
      # Get color based on class ID
      color = CLASS_COLORS[self.class_id % len(CLASS_COLORS)]
      # Highlight selected boxes with white
      if self.selected:
          color = (255, 255, 255)
      x1, y1, x2, y2 = self.get_rect()
      x1, y1 = max(0, x1), max(0, y1)
      x2, y2 = min(img.shape[1], x2), min(img.shape[0], y2)
      cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
      for handle in self.get_handles().values():
          if 0 <= handle[0] < img.shape[1] and 0 <= handle[1] < img.shape[0]:
              cv2.circle(img, handle, 5, color, -1)
      cv2.putText(img, CLASS_NAMES[self.class_id], (x1, max(0, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

# ----------------- Helper Functions ------------------
def yolo_to_box(line, img_w, img_h):
    parts = line.strip().split()
    cid = int(parts[0])
    xc, yc, w, h = map(float, parts[1:])
    x = int((xc - w / 2) * img_w)
    y = int((yc - h / 2) * img_h)
    return BoundingBox(cid, x, y, int(w * img_w), int(h * img_h))

def box_to_yolo(bbox, img_w, img_h):
    xc = (bbox.x + bbox.w / 2) / img_w
    yc = (bbox.y + bbox.h / 2) / img_h
    w = bbox.w / img_w
    h = bbox.h / img_h
    return f"{bbox.class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}"

def apply_zoom(img):
    h, w = img.shape[:2]
    new_w, new_h = int(w * zoom), int(h * zoom)
    if new_w < 10 or new_h < 10:
        return img.copy()
    resized = cv2.resize(img, (new_w, new_h))
    pan_x_clamped = max(0, min(pan_x, max(0, resized.shape[1] - w)))
    pan_y_clamped = max(0, min(pan_y, max(0, resized.shape[0] - h)))
    display = resized[pan_y_clamped:pan_y_clamped + h, pan_x_clamped:pan_x_clamped + w]
    return display

def translate_coords(x, y):
    return int((x + pan_x) / zoom), int((y + pan_y) / zoom)

def get_box_at_pos(x, y):
    for box in reversed(boxes):
        for name, (hx, hy) in box.get_handles().items():
            if abs(x - hx) < 8 and abs(y - hy) < 8:
                box.selected = True
                box.handle_selected = name
                return box
        x1, y1, x2, y2 = box.get_rect()
        if x1 <= x <= x2 and y1 <= y <= y2:
            box.selected = True
            box.handle_selected = 'move'
            return box
    return None

# ----------------- Mouse Callback ------------------
def mouse_callback(event, x, y, flags, param):
    global dragging, selected_box, start_x, start_y, cursor_x, cursor_y
    global adding_box, new_box_start, new_box_current, zoom, pan_x, pan_y
    cursor_x, cursor_y = x, y
    real_x, real_y = translate_coords(x, y)

    if adding_box:
        if event == cv2.EVENT_LBUTTONDOWN:
            new_box_start = (real_x, real_y)
            new_box_current = (real_x, real_y)
        elif event == cv2.EVENT_MOUSEMOVE and new_box_start:
            new_box_current = (real_x, real_y)
        elif event == cv2.EVENT_LBUTTONUP and new_box_start:
            x0, y0 = new_box_start
            x1, y1 = new_box_current
            w, h = x1 - x0, y1 - y0
            if w < 0: x0 += w; w = -w
            if h < 0: y0 += h; h = -h
            boxes.append(BoundingBox(0, x0, y0, w, h))
            adding_box = False
            new_box_start = None
            new_box_current = None

    elif event == cv2.EVENT_LBUTTONDOWN:
        for box in boxes:
            box.selected = False
        selected_box = get_box_at_pos(real_x, real_y)
        if selected_box:
            dragging = True
            start_x, start_y = real_x, real_y

    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging and selected_box:
            dx = real_x - start_x
            dy = real_y - start_y
            h = selected_box.handle_selected
            if h == 'move':
                selected_box.x += dx
                selected_box.y += dy
            elif h == 'tl': selected_box.x += dx; selected_box.y += dy; selected_box.w -= dx; selected_box.h -= dy
            elif h == 'tr': selected_box.w += dx; selected_box.y += dy; selected_box.h -= dy
            elif h == 'bl': selected_box.x += dx; selected_box.w -= dx; selected_box.h += dy
            elif h == 'br': selected_box.w += dx; selected_box.h += dy
            elif h == 'l': selected_box.x += dx; selected_box.w -= dx
            elif h == 'r': selected_box.w += dx
            elif h == 't': selected_box.y += dy; selected_box.h -= dy
            elif h == 'b': selected_box.h += dy
            start_x, start_y = real_x, real_y

    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False
        if selected_box:
            if selected_box.w < 0: selected_box.x += selected_box.w; selected_box.w *= -1
            if selected_box.h < 0: selected_box.y += selected_box.h; selected_box.h *= -1
            selected_box.handle_selected = None

    elif event == cv2.EVENT_MOUSEWHEEL:
        old_zoom = zoom
        zoom += zoom_step if flags > 0 else -zoom_step
        zoom = max(min_zoom, min(max_zoom, zoom))
        ratio = zoom / old_zoom
        pan_x = int((cursor_x + pan_x) * ratio - cursor_x)
        pan_y = int((cursor_y + pan_y) * ratio - cursor_y)

# ----------------- Main Loop ------------------
while current_image_index < len(image_files):
    file = image_files[current_image_index]
    path = os.path.join(IMAGE_FOLDER, file)
    label_path = os.path.join(LABEL_FOLDER, os.path.splitext(file)[0] + ".txt")
    img = cv2.imread(path)
    img_h, img_w = img.shape[:2]
    boxes = []
    selected_box = None
    if os.path.exists(label_path):
        with open(label_path) as f:
            boxes = [yolo_to_box(line, img_w, img_h) for line in f]

    cv2.namedWindow(file)
    cv2.setMouseCallback(file, mouse_callback)
    while True:
        temp = img.copy()
        for box in boxes:
            box.draw(temp)

        # Draw preview new box during add mode
        if adding_box and new_box_start and new_box_current:
            x0, y0 = new_box_start
            x1, y1 = new_box_current
            cv2.rectangle(temp, (x0, y0), (x1, y1), (0, 255, 255), 2)
            cv2.putText(temp, CLASS_NAMES[0], (x0, y0 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        display = apply_zoom(temp)
        if display.shape[0] == 0 or display.shape[1] == 0:
            zoom = 1.0
            pan_x, pan_y = 0, 0
            display = img.copy()
        cv2.imshow(file, display)
        key = cv2.waitKey(1) & 0xFF

        if selected_box and (chr(key) in CLASS_KEYS):
            selected_box.class_id = CLASS_KEYS[chr(key)]
            print(f"Class changed to: {CLASS_NAMES[selected_box.class_id]}")
        elif key == ord('d') and selected_box:
            boxes.remove(selected_box)
            selected_box = None
            print("Box deleted.")
        elif key == ord('a'):
            adding_box = True
            new_box_start = None
            new_box_current = None
            print("Add mode: Click + drag to draw box")
        elif key == ord('s'):
            with open(label_path, 'w') as f:
                for box in boxes:
                    f.write(box_to_yolo(box, img_w, img_h) + "\n")
            print("Saved.")
        elif key == ord('n'):
            current_image_index += 1
            break
        elif key == ord('b') and current_image_index > 0:
            current_image_index -= 1
            break
        elif key == ord('x'):
            cv2.destroyAllWindows()
            exit()
        elif key == 81: pan_x = max(0, pan_x - 20)
        elif key == 82: pan_y = max(0, pan_y - 20)
        elif key == 83: pan_x += 20
        elif key == 84: pan_y += 20
    cv2.destroyAllWindows()