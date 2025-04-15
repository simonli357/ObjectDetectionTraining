from augmentations import *
import os

def apply_random_from_group(image, group_id, image_path=None):
    if group_id == 1:
        func = random.choice([strong_color_shift,adjust_brightness, apply_color_temperature])
        if func == strong_color_shift:
            return func(image, image_path)  # pass the path for folder-based logic
        return func(image)
    elif group_id == 2:
        return apply_desaturation(image)
    elif group_id == 3:
        return random.choice([adjust_contrast_blend, adjust_contrast])(image)
    elif group_id == 4:
        return apply_motion_blur(image)
    elif group_id == 5:
        return random.choice([apply_defocus_blur])(image)
    elif group_id == 6:
        func = random.choice([apply_albumentations_enhancements, lambda x, *_: x])
        if func == strong_color_shift:
            return func(image, image_path)  # pass the path for folder-based logic
        return func(image)
    elif group_id == 7:
        return random.choice([rotate, perspective_warp])(image)
    elif group_id == 8:
        return random.choice([apply_pixelation])(image)
    return image


def apply_transformations_to_directory(directory, output_dir):
    can_flip = True
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(directory, filename)
            image = cv2.imread(path)
            image1 = image.copy()
            if can_flip and random.random() < 0.5:
                image1 = flip_lr(image)
            # cv2.imwrite(os.path.join(output_dir, filename), image1)
            name, ext = os.path.splitext(filename)

            for suffix in ['a', 'b', 'c']:
                transformed = image.copy()
                chosen_groups = random.sample(range(1, 8), 2)
                for group in chosen_groups:
                    if can_flip and random.random() < 0.5:
                        transformed = flip_lr(transformed)
                    transformed = apply_random_from_group(transformed, group, image_path=path)
                new_path = os.path.join(output_dir, f"{name}{suffix}{ext}")
                cv2.imwrite(new_path, transformed)

CLASS_NAMES = ["oneway", "highwayentrance", "stopsign", "roundabout", "park",
               "crosswalk", "noentry", "highwayexit", "prio", "light",
               "roadblock", "girl", "cars2"]
if __name__ == "__main__":
    id = 5
    target_number = 12000
    # folder_path = '/media/slsecret/E624108524105B3F/Users/simon/Downloads/cars/crosswalk'
    # folder_path = '/home/slsecret/Downloads/bfmc_data/cropped/crosswalk'
    folder_path = '/home/slsecret/Downloads/bfmc_data/cropped/' + CLASS_NAMES[id]
    output_path = folder_path + '_augmented'
    os.makedirs(output_path, exist_ok=True)
    apply_transformations_to_directory(folder_path, output_path)