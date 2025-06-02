import cv2

# Open the webcam (device 0)
cap = cv2.VideoCapture(0)

# Set resolution (adjust if needed)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Mirror the frame horizontally
    frame = cv2.flip(frame, 1)

    # Show the frame in a window
    cv2.imshow("Karen's Vision", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
