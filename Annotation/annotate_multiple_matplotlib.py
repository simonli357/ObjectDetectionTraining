import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from matplotlib.backend_bases import MouseButton

# Folder paths
image_folder = '/home/slsecret/Downloads/bfmc_data/images/misc'
labels_folder = '/home/slsecret/Downloads/bfmc_data/images/misc_labels'
os.makedirs(labels_folder, exist_ok=True)

# Class names and color map
class_names = [
    "oneway", "highwayentrance", "stop", "roundabout", "parking",
    "crosswalk", "noentry", "highwayexit", "prio", "light",
    "block", "girl", "car"
]
class_colors = ['b', 'g', 'r', 'y', 'm', 'c', 'maroon', 'darkgreen', 'navy',
                'olive', 'purple', 'teal', 'gray']

current_class = 0
image_index = 0
bounding_boxes = []

class Annotator:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.current_image = None
        self.image_name = ''
        self.img_width = 0
        self.img_height = 0
        self.start_point = None
        self.zoom = 1.0

        self.fig, self.ax = plt.subplots()
        self.rect = None
        self.preview_rect = None
        self.pressed = False
        self.annotations = []
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_scroll = self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.load_image()

    def load_image(self):
        global bounding_boxes
        if image_index >= len(self.image_paths):
            print("Done!")
            plt.close()
            return

        path = self.image_paths[image_index]
        img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        self.img_height, self.img_width = img.shape[:2]
        self.current_image = img
        self.image_name = os.path.basename(path)
        self.ax.clear()
        self.ax.imshow(img)
        self.ax.set_title(f"{self.image_name} | Class: {class_names[current_class]}")
        self.annotations = []
        bounding_boxes = []
        self.preview_rect = None
        self.start_point = None
        txt_path = os.path.join(labels_folder, os.path.splitext(self.image_name)[0] + ".txt")
        if os.path.exists(txt_path):
            print(f"Skipping {self.image_name} (already annotated)")
            self.next_image()
        self.fig.canvas.draw()

    def on_press(self, event):
        if event.inaxes != self.ax or event.button != MouseButton.LEFT:
            return
        self.start_point = (event.xdata, event.ydata)
        self.pressed = True

    def on_motion(self, event):
        if not self.pressed or self.start_point is None or event.inaxes != self.ax:
            return
        x0, y0 = self.start_point
        x1, y1 = event.xdata, event.ydata
        width = x1 - x0
        height = y1 - y0
        if self.preview_rect:
            self.preview_rect.remove()
        self.preview_rect = patches.Rectangle((x0, y0), width, height,
                                              linewidth=1, edgecolor=class_colors[current_class],
                                              facecolor='none', linestyle='--')
        self.ax.add_patch(self.preview_rect)
        self.fig.canvas.draw()

    def on_release(self, event):
        if not self.pressed or self.start_point is None or event.button != MouseButton.LEFT:
            return
        x0, y0 = self.start_point
        x1, y1 = event.xdata, event.ydata
        self.pressed = False
        self.start_point = None
        if self.preview_rect:
            self.preview_rect.remove()
            self.preview_rect = None
        xmin, xmax = sorted([x0, x1])
        ymin, ymax = sorted([y0, y1])
        width = xmax - xmin
        height = ymax - ymin
        if width > 5 and height > 5:
            self.annotations.append((current_class, xmin, ymin, width, height))
            rect = patches.Rectangle((xmin, ymin), width, height,
                                     linewidth=2, edgecolor=class_colors[current_class],
                                     facecolor='none')
            self.ax.add_patch(rect)
            self.ax.text(xmin, ymin - 5, class_names[current_class], fontsize=8,
                         color=class_colors[current_class])
            self.fig.canvas.draw()

    def on_scroll(self, event):
        if event.button == 'up':
            self.zoom *= 1.1
        elif event.button == 'down':
            self.zoom /= 1.1
        self.ax.set_xlim(event.xdata - self.img_width / self.zoom / 2,
                         event.xdata + self.img_width / self.zoom / 2)
        self.ax.set_ylim(event.ydata + self.img_height / self.zoom / 2,
                         event.ydata - self.img_height / self.zoom / 2)
        self.fig.canvas.draw()

    def on_key(self, event):
        global current_class, image_index

        # Pan step adjusts depending on zoom level
        pan_step = 50 / self.zoom

        if event.key.isdigit():
            current_class = int(event.key)
            if current_class < len(class_names):
                print(f"Switched to class: {class_names[current_class]}")
                self.ax.set_title(f"{self.image_name} | Class: {class_names[current_class]}")
                self.fig.canvas.draw()

        elif event.key == 's':
            self.save_annotations()
            self.next_image()

        elif event.key == 'r':
            if self.annotations:
                self.annotations.pop()
                self.redraw()

        elif event.key == 'q':
            print("Exiting...")
            plt.close()

        # ⬅ Pan Left
        elif event.key == 'left':
            xlim = self.ax.get_xlim()
            self.ax.set_xlim(xlim[0] - pan_step, xlim[1] - pan_step)
            self.fig.canvas.draw()

        # ➡ Pan Right
        elif event.key == 'right':
            xlim = self.ax.get_xlim()
            self.ax.set_xlim(xlim[0] + pan_step, xlim[1] + pan_step)
            self.fig.canvas.draw()

        # ⬆ Pan Up
        elif event.key == 'up':
            ylim = self.ax.get_ylim()
            self.ax.set_ylim(ylim[0] - pan_step, ylim[1] - pan_step)
            self.fig.canvas.draw()

        # ⬇ Pan Down
        elif event.key == 'down':
            ylim = self.ax.get_ylim()
            self.ax.set_ylim(ylim[0] + pan_step, ylim[1] + pan_step)
            self.fig.canvas.draw()

    def redraw(self):
        self.ax.clear()
        self.ax.imshow(self.current_image)
        for annotation in self.annotations:
            obj_id, x, y, w, h = annotation
            rect = patches.Rectangle((x, y), w, h,
                                     linewidth=2, edgecolor=class_colors[obj_id], facecolor='none')
            self.ax.add_patch(rect)
            self.ax.text(x, y - 5, class_names[obj_id], fontsize=8, color=class_colors[obj_id])
        self.ax.set_title(f"{self.image_name} | Class: {class_names[current_class]}")
        self.fig.canvas.draw()

    def save_annotations(self):
        txt_path = os.path.join(labels_folder, os.path.splitext(self.image_name)[0] + ".txt")
        with open(txt_path, 'w') as f:
            for bbox in self.annotations:
                obj_id, x, y, w, h = bbox
                x_center = (x + w / 2) / self.img_width
                y_center = (y + h / 2) / self.img_height
                w_norm = w / self.img_width
                h_norm = h / self.img_height
                f.write(f"{obj_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
        print(f"Saved: {txt_path}")

    def next_image(self):
        global image_index
        image_index += 1
        self.load_image()


# Run
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))])
image_paths = [os.path.join(image_folder, f) for f in image_files]

if not image_paths:
    print("No images found.")
else:
    tool = Annotator(image_paths)
    plt.show()
