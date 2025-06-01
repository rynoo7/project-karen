import cv2
import os

# Create folder for calibration frames
calib_dir = "/home/ryn007/Programs/Karen/Calibration"
os.makedirs(calib_dir, exist_ok=True)

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("=== Karen Calibration Mode ===")
print("Press SPACE to take a photo. Press ESC when done.")

img_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error capturing frame.")
        break

    frame = cv2.flip(frame, 1)  # mirror it
    cv2.imshow("Karen Calibration View", frame)

    key = cv2.waitKey(1)

    if key % 256 == 27:  # ESC
        break
    elif key % 256 == 32:  # SPACE
        filename = os.path.join(calib_dir, f"frame_{img_count:02d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Captured {filename}")
        img_count += 1

cap.release()
cv2.destroyAllWindows()
print("Capturing complete. Attempting to stitch...")

# Load all captured frames
images = []
for i in range(img_count):
    path = os.path.join(calib_dir, f"frame_{i:02d}.jpg")
    img = cv2.imread(path)
    if img is not None:
        images.append(img)

# Stitch the images into a panorama
stitcher = cv2.Stitcher_create()
status, pano = stitcher.stitch(images)

if status == cv2.Stitcher_OK:
    output_path = "/home/ryn007/Programs/Karen/Photos/GARAGE.jpg"
    cv2.imwrite(output_path, pano)
    print(f"Panorama saved to {output_path}")
else:
    print("Stitching failed. Try taking photos with more overlap.")
