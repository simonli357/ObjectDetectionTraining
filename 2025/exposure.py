import cv2
import numpy as np

# Constants
TARGET_MSV = 2.5
NUM_BINS = 256
HIST_REGIONS = 5
MAX_GAIN = 127
MAX_EXPOSURE = 511

# Simulated camera parameters
exposure = 100
gain = 1

# PI Controller setup
class PIController:
    def __init__(self, Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki
        self.integral = 0.0

    def update(self, error):
        self.integral += error
        return self.Kp * error + self.Ki * self.integral

# Create mask (circular area of interest)
def create_circular_mask(h, w, radius_ratio=0.5):
    center = (int(w/2), int(h/2))
    radius = int(min(h, w) * radius_ratio)
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    mask = dist_from_center <= radius
    return mask.astype(np.uint8) * 255

# Calculate Mean Sample Value (MSV)
def calculate_msv(hist):
    region_size = NUM_BINS // HIST_REGIONS
    xi = [np.sum(hist[i*region_size:(i+1)*region_size]) for i in range(HIST_REGIONS)]
    numerator = sum((i + 1) * x for i, x in enumerate(xi))
    denominator = sum(xi)
    return numerator / denominator if denominator != 0 else 0

# Initialize webcam
cap = cv2.VideoCapture(0)
controller_exposure = PIController(Kp=5, Ki=0.1)
controller_gain = PIController(Kp=2, Ki=0.05)

# Create mask once (same size as frame)
ret, frame = cap.read()
h, w = frame.shape[:2]
mask = create_circular_mask(h, w)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply mask
    masked = cv2.bitwise_and(gray, gray, mask=mask)

    # Compute histogram
    hist = cv2.calcHist([masked], [0], mask, [NUM_BINS], [0, 256])
    hist = cv2.normalize(hist, hist).flatten()

    # Calculate MSV
    msv = calculate_msv(hist)

    # Compute error
    error = TARGET_MSV - msv

    # Update simulated exposure/gain
    if exposure < MAX_EXPOSURE:
        exposure_change = controller_exposure.update(error)
        exposure = np.clip(exposure + exposure_change, 0, MAX_EXPOSURE)
    else:
        gain_change = controller_gain.update(error)
        gain = np.clip(gain + gain_change, 1, MAX_GAIN)

    # Simulate change (visualize)
    simulated = cv2.convertScaleAbs(gray, alpha=gain / 10, beta=exposure / 10)

    # Show visualizations
    cv2.imshow("Original", frame)
    cv2.imshow("Masked", masked)
    cv2.imshow("Simulated Exposure", simulated)

    print(f"MSV: {msv:.2f} | Exposure: {exposure:.0f} | Gain: {gain:.0f}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
