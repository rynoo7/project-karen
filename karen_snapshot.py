import cv2

# Open webcam
cap = cv2.VideoCapture(0)

# Wait for the camera to warm up
ret, frame = cap.read()
if not ret:
    print("Failed to capture image.")
    cap.release()
    exit()

# Mirror the image
frame = cv2.flip(frame, 1)

# Save to file
filename = "/home/ryn007/Programs/Karen/Photos/karen_snapshot.jpg"
cv2.imwrite(filename, frame)
print(f"Snapshot saved to {filename}")

cap.release()
