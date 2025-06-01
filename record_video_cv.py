#!/usr/bin/env python3
import cv2
import time
from datetime import datetime

cap = cv2.VideoCapture(0)
time.sleep(0.2)

# Set resolution and FPS
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = 20
duration = 10  # seconds

# Create video writer
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"/home/ryn007/Programs/Karen/Recordings/video_{timestamp}.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))

print(f"[Karen] Recording to: {filename}")

start_time = time.time()
while time.time() - start_time < duration:
    ret, frame = cap.read()
    if ret:
        out.write(frame)
    else:
        break

out.release()
cap.release()
print("[Karen] Done recording.")
