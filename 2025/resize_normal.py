#!/usr/bin/env python3
import os
import sys
import glob
import argparse
from PIL import Image
import numpy as np
from scipy.stats import truncnorm

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=("Resize images in a folder so that, when sorted by original width, the target widths "
                     "follow a truncated normal distribution with a specified mean and standard deviation, "
                     "confined to fixed bounds of 20 and 200 pixels. No image is ever upscaled, only downscaled "
                     "as necessary.")
    )
    parser.add_argument("--mean", type=float, default=100,
                        help="Mean target width (default=100)")
    parser.add_argument("--std", type=float, default=60,
                        help="Standard deviation of target widths (default=60)")
    return parser.parse_args()

def get_image_files(folder):
    # Look for common image file extensions.
    exts = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "*.tiff"]
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(folder, ext)))
    return files

def main():
    args = parse_arguments()

    # Set the input and output folders (update these paths as required).
    input_folder = "/media/slsecret/E624108524105B3F/Users/simon/Downloads/cars/prio/"
    output_folder = "/media/slsecret/E624108524105B3F/Users/simon/Downloads/cars/prio_resized_normal/"
    
    mean_val = args.mean
    std_val = args.std

    # Fixed clipping bounds.
    lower_bound = 20
    upper_bound = 200

    # Compute parameters for the truncated normal distribution.
    a = (lower_bound - mean_val) / std_val
    b = (upper_bound - mean_val) / std_val

    os.makedirs(output_folder, exist_ok=True)

    # Retrieve all image files.
    image_files = get_image_files(input_folder)
    if not image_files:
        print("No images found in:", input_folder)
        sys.exit(1)

    # Gather image information (original dimensions).
    images_info = []
    for filepath in image_files:
        try:
            with Image.open(filepath) as im:
                w, h = im.size
            images_info.append({"path": filepath, "width": w, "height": h})
        except Exception as e:
            print(f"Could not open {filepath}: {e}")

    if not images_info:
        print("No valid images found!")
        sys.exit(1)

    # Sort images by original width (ascending order).
    images_info.sort(key=lambda x: x["width"])
    n = len(images_info)
    print(f"Processing {n} images...")

    # Process each image using the truncated normal distribution for mapping.
    for i, info in enumerate(images_info):
        orig_width = info["width"]
        orig_height = info["height"]

        # Compute the rank-based probability (using mid-point of each rank bin).
        p = (i + 0.5) / n

        # Compute target width using the truncated normal distribution's inverse CDF.
        target_width = truncnorm.ppf(p, a, b, loc=mean_val, scale=std_val)
        
        # Only allow downscaling: if computed target is higher than original width, keep original.
        target_w = int(round(target_width)) if target_width <= orig_width else orig_width

        # Maintain aspect ratio.
        scale = target_w / orig_width
        target_h = int(round(orig_height * scale))
        
        try:
            with Image.open(info["path"]) as im:
                im_resized = im.resize((target_w, target_h), Image.LANCZOS)
                base_name = os.path.basename(info["path"])
                output_path = os.path.join(output_folder, base_name)
                im_resized.save(output_path)
                print(f"Processed {base_name}: original {orig_width}x{orig_height}, target {target_w}x{target_h}")
        except Exception as e:
            print(f"Failed to process {info['path']}: {e}")

    print("All images have been processed and saved in:", output_folder)

    # Optional: Analyze the resized image widths
    resized_widths = []
    for file in os.listdir(output_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                with Image.open(os.path.join(output_folder, file)) as img:
                    width, _ = img.size
                    resized_widths.append(width)
            except Exception as e:
                print(f"Error reading {file}: {e}")

    if resized_widths:
        print("\n=== Resized Image Stats ===")
        print(f"Total resized images: {len(resized_widths)}")
        print(f"Min width     : {min(resized_widths)} px")
        print(f"Max width     : {max(resized_widths)} px")
        print(f"Mean width    : {np.mean(resized_widths):.2f} px")
        print(f"Std deviation : {np.std(resized_widths):.2f} px")
        
        # Create a histogram with 10-pixel bin sizes.
        hist, edges = np.histogram(resized_widths, bins=np.arange(min(resized_widths), max(resized_widths)+11, 10))
        print("\nWidth histogram (10 px bins):")
        for count, edge_start, edge_end in zip(hist, edges[:-1], edges[1:]):
            percentage = (count / sum(hist)) * 100
            print(f"{int(edge_start):4d}-{int(edge_end - 1):4d} px: {percentage:6.2f}%")
    else:
        print("No resized images found to analyze.")

if __name__ == "__main__":
    main()
