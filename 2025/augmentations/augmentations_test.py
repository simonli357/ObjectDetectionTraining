import cv2
import numpy as np
import albumentations as A
from albumentations.augmentations.transforms import RandomSunFlare, RandomFog, RandomRain, RandomSnow, RandomBrightnessContrast, HueSaturationValue

# -----------------------------
# Augmentation Utility Functions
# -----------------------------

def apply_motion_blur(image, kernel_size=15):
    # Applies motion blur by averaging pixels in a horizontal line of length kernel_size
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[kernel_size // 2, :] = 1.0
    kernel = kernel / kernel_size
    return cv2.filter2D(image, -1, kernel)

def apply_pixelation(image, scale=0.25):
    # Downscales and upscales the image to simulate pixelation (blocky blur)
    h, w = image.shape[:2]
    small = cv2.resize(image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

def apply_defocus_blur(image, ksize=7):
    # Simulates camera defocus blur; ksize controls the blur strength
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    # alpha > 1.0 increases contrast, < 1.0 reduces contrast
    # beta > 0 brightens, < 0 darkens the image
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def adjust_contrast_blend(image, contrast_factor=0.5):
    # Blends image with gray to reduce contrast; lower contrast_factor = flatter image
    gray = np.full_like(image, np.mean(image, dtype=np.uint8))
    return cv2.addWeighted(image, contrast_factor, gray, 1 - contrast_factor, 0)

def apply_desaturation(image, strength=0.5):
    # Converts image toward grayscale based on strength (0=no change, 1=fully grayscale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_three = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    return cv2.addWeighted(image, 1 - strength, gray_three, strength, 0)

def apply_color_temperature(image, warm_factor=0.1):
    # Increases red, decreases blue to create a warm effect (simulates sunlight)
    img = image.astype(np.float32)
    img[..., 2] *= 1 + warm_factor  # Red channel
    img[..., 0] *= 1 - warm_factor  # Blue channel
    return np.clip(img, 0, 255).astype(np.uint8)

def apply_sun(image, alpha=0.5):
    # Simulates sun glare + flare using overlay and Albumentations
    h, w = image.shape[:2]
    overlay = np.zeros((h, w, 3), dtype=np.uint8)
    center = (int(w * 0.5), int(h * 0.2))
    radius = int(min(h, w) * 0.3)
    cv2.circle(overlay, center, radius, (255, 255, 255), -1)
    overlay = cv2.GaussianBlur(overlay, (151, 151), 0)
    image = cv2.addWeighted(image, 1, overlay, alpha, 0)
    aug = A.Compose([
        RandomSunFlare(flare_roi=(0.1, 0.1, 0.9, 0.4), angle_lower=0.5, num_flare_circles_lower=6, 
                       num_flare_circles_upper=10, src_radius=100, src_color=(255, 255, 255), always_apply=True)
    ])
    return aug(image=image)['image']

def apply_rain(image):
    # Adds synthetic rain streaks and brightness adjustment
    aug = A.Compose([
        RandomRain(blur_value=2, brightness_coefficient=0.8, always_apply=True)
    ])
    return aug(image=image)['image']

def apply_albumentations_enhancements(image):
    # Randomly adjusts brightness, contrast, hue, saturation, and value
    aug = A.Compose([
        RandomBrightnessContrast(p=1.0),
        HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=1.0)
    ])
    return aug(image=image)['image']

def reduce_contrast(image, factor=0.6):
    # Reduces image contrast by blending it with gray; lower factor = more reduction
    gray = np.full_like(image, np.mean(image, dtype=np.uint8))
    return cv2.addWeighted(image, factor, gray, 1 - factor, 0)

def apply_color_cast(image, red_scale=0.95, green_scale=1.1, blue_scale=1.05):
    # Applies manual scaling to RGB channels to simulate color tinting
    image = image.astype(np.float32)
    image[..., 0] *= blue_scale   # Blue
    image[..., 1] *= green_scale  # Green
    image[..., 2] *= red_scale    # Red
    return np.clip(image, 0, 255).astype(np.uint8)

def add_haze(image, intensity=0.3):
    # Adds a white haze to simulate fog or lens dirtiness
    h, w = image.shape[:2]
    haze = np.full((h, w, 3), 255, dtype=np.uint8)
    return cv2.addWeighted(image, 1 - intensity, haze, intensity, 0)

def strong_color_shift(image):
    # Aggressively shifts RGB channels for a more drastic color cast
    img = image.astype(np.float32)
    img[..., 0] *= 1.3   # Boost blue
    img[..., 1] *= 1.2   # Boost green
    img[..., 2] *= 0.6   # Reduce red
    return np.clip(img, 0, 255).astype(np.uint8)

def push_highlights(image, threshold=200):
    # Clamps bright areas above threshold to white to simulate blown highlights
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = hsv[..., 2] > threshold
    hsv[..., 2][mask] = 255
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def haze_blur(image, haze_intensity=0.3):
    # Applies Gaussian blur and white haze overlay to simulate environmental fog
    blurred = cv2.GaussianBlur(image, (5, 5), sigmaX=2)
    white_haze = np.full_like(blurred, 255)
    return cv2.addWeighted(blurred, 1 - haze_intensity, white_haze, haze_intensity, 0)

# -----------------------------
# Main for Testing Augmentations
# -----------------------------

if __name__ == "__main__":
    import os
    image_path = '/media/slsecret/E624108524105B3F/Users/simon/Downloads/cars/stopsign/16.JPG'
    image_path = '/media/slsecret/E624108524105B3F/Users/simon/Downloads/cars/crosswalk/20.JPG'
    image = cv2.imread(image_path)

    cv2.imshow('Original', image)
    cv2.imshow('Motion Blur', apply_motion_blur(image.copy(), kernel_size=40))
    cv2.imshow('Pixelated', apply_pixelation(image.copy(), scale=0.3))
    cv2.imshow('Defocus Blur', apply_defocus_blur(image.copy(), ksize=11))
    cv2.imshow('Brighter', adjust_brightness_contrast(image.copy(), alpha=1.0, beta=90))
    cv2.imshow('Darker', adjust_brightness_contrast(image.copy(), alpha=1.0, beta=-90))
    cv2.imshow('Higher Contrast', adjust_brightness_contrast(image.copy(), alpha=1.5, beta=0))
    cv2.imshow('Lower Contrast', adjust_contrast_blend(image.copy(), contrast_factor=0.5))
    cv2.imshow('Desaturated', apply_desaturation(image.copy(), strength=0.7))
    cv2.imshow('Warm Tone', apply_color_temperature(image.copy(), warm_factor=0.4))
    cv2.imshow('Rain Effect', apply_rain(image.copy()))
    cv2.imshow('Sun Flare Effect', apply_sun(image.copy(), alpha=0.5))
    cv2.imshow('Albumentations Enhancements', apply_albumentations_enhancements(image.copy()))

    shifted = strong_color_shift(image)
    highlighted = push_highlights(shifted)
    # hazy = haze_blur(highlighted, haze_intensity=0.35)

    cv2.imshow("Closer Match Simulation", highlighted)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
