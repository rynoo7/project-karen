#!/usr/bin/env python3

import cv2
import time
from datetime import datetime

# Connect to camera feed (already open in main app)
cap = cv2.VideoCapture(0)

# Wait briefly to ensure the feed is ready
time.sleep(0.1)
ret, frame = cap.read()
if ret:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/home/ryn007/Programs/Karen/Recordings/photo_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[Karen] Snapshot saved to: {filename}")
else:
    print("[Karen] Failed to capture frame.")

cap.release()
