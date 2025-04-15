import cv2
import numpy as np
import os
# Load the clean crosswalk image
image = cv2.imread("/media/slsecret/E624108524105B3F/Users/simon/Downloads/cars/crosswalk/18.JPG")  # change to your file path

# Step 1: Gaussian Blur (simulate defocus)
blurred = cv2.GaussianBlur(image, (5, 5), 2)

# Step 2: Downscale and Upscale (simulate pixelation / low resolution)
h, w = blurred.shape[:2]
pixelated = cv2.resize(blurred, (w // 6, h // 6), interpolation=cv2.INTER_LINEAR)
pixelated = cv2.resize(pixelated, (w, h), interpolation=cv2.INTER_NEAREST)

# Step 3: Add Gaussian Noise (simulate sensor/environment noise)
# noise = np.random.normal(0, 20, pixelated.shape).astype(np.uint8)
# noisy = cv2.add(pixelated, noise)

# Step 4: Adjust brightness and contrast (simulate lighting/glare)
bright = cv2.convertScaleAbs(pixelated, alpha=1.4, beta=35)

# Step 5: Perspective warp (simulate viewing angle)
# pts1 = np.float32([[0, 0], [200, 0], [0, 200], [200, 200]])
# pts2 = np.float32([[20, 10], [180, 0], [0, 200], [200, 180]])
# matrix = cv2.getPerspectiveTransform(pts1, pts2)
# warped = cv2.warpPerspective(bright, matrix, (200, 200))

# Step 6 (Optional): Desaturate (simulate faded color)
desaturated = cv2.cvtColor(bright, cv2.COLOR_BGR2HSV)
desaturated[..., 1] = desaturated[..., 1] * 0.6  # reduce saturation
final = cv2.cvtColor(desaturated, cv2.COLOR_HSV2BGR)

# Save or display
cv2.imwrite("crosswalk_simulated.png", final)
cv2.imshow("Simulated Crosswalk", final)
cv2.waitKey(0)
cv2.destroyAllWindows()
