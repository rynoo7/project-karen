import pygame
import sys
import os
import cv2
import time
import subprocess
from datetime import datetime
import threading

class VideoRecorder(threading.Thread):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.running = True
        self.frames = []
        self.start_time = time.time()
        self.duration = 10  # seconds
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_path = f"/home/ryn007/Programs/Karen/Recordings/video_only_{timestamp}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.output_path, fourcc, 20.0, (width, height))

    def run(self):
        while self.running and (time.time() - self.start_time) < self.duration:
            if current_frame is not None:
                frame_resized = cv2.resize(current_frame, (self.width, self.height))
                self.out.write(frame_resized)
            time.sleep(1/20.0)  # Simulate ~20 FPS

        self.out.release()
        print(f"[Karen] Video saved: {self.output_path}")

    def stop(self):
        self.running = False


# Initialize Pygame and OpenCV
pygame.init()

# Webcam capture setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Screen and image loading
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Karen's Living Memory")

# Load and scale panoramic image
image_path = "/home/ryn007/Programs/Karen/Photos/GARAGE.jpg"
background = pygame.image.load(image_path).convert()
img_width, img_height = background.get_size()
scale_factor = screen_height / img_height
scaled_width = int(img_width * scale_factor)
scaled_image = pygame.transform.scale(background, (scaled_width, screen_height))

# Define scroll range
scroll_x = 0
max_scroll_x = scaled_width - screen_width

# Define where the webcam feed goes in the image (image coordinates)
LIVE_FEED_RECT = pygame.Rect(4295, 380, 355, 220)

# Define interactive zones
zones = [
    (pygame.Rect(3498, 647, 260, 400), "/home/ryn007/Programs/Karen/Photos/Mobile_toolbox.jpg"),
    (pygame.Rect(4376, 670, 185, 265), "/home/ryn007/Programs/Karen/Photos/Karen.jpg"),
    
    (pygame.Rect(4415, 320, 115, 60), "snapshot"),
    (pygame.Rect(4300, 390, 350, 200), "python3 /home/ryn007/Programs/Karen/record_video_cv.py"),
    
    #(pygame.Rect(4705, 20, 760, 1050), "/home/ryn007/Programs/Karen/Photos/golfcart.jpg"),
    (pygame.Rect(4705, 20, 760, 1050), "/home/ryn007/Projects/Golf_Cart_Project/Golf_Cart_Motor_Controller_Overview.pdf"),

    #Active Projects Box
    (pygame.Rect(3232, 868, 218, 17), "/home/ryn007/Programs/Karen/Photos/active_projects_box.jpg"),

    (pygame.Rect(3188, 550, 280, 150), "/home/ryn007/Programs/Karen/Photos/BallBearing_toolbox.jpg"),
    (pygame.Rect(2800, 530, 395, 230), "/home/ryn007/Programs/Karen/Photos/Mongoose_toolbox.jpg"),
    (pygame.Rect(1970, 490, 530, 450), "/home/ryn007/Programs/Karen/Photos/Paint_shelf.jpg"),
    (pygame.Rect(145, 612, 185, 270), "/home/ryn007/Programs/Karen/Photos/Eileen.jpg"),
]

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scroll_x = int((mouse_x / screen_width) * max_scroll_x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            image_x = scroll_x + mouse_x
            image_y = mouse_y
            for rect, path in zones:
                if rect.collidepoint(image_x, image_y):
                    if "record_video" in path:
                        print("[Karen] Recording video from live feed...")
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        video_path = f"/home/ryn007/Programs/Karen/Recordings/video_{timestamp}.mp4"
                        audio_path = f"/home/ryn007/Programs/Karen/Recordings/audio_{timestamp}.wav"
                        output_path = f"/home/ryn007/Programs/Karen/Recordings/karen_memory_{timestamp}.mp4"

                        # Start recording audio in the background
                        audio_proc = subprocess.Popen(
                            ["ffmpeg", "-f", "alsa", "-i", "default", "-t", "10", audio_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )

                        # Record video with OpenCV
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        out = cv2.VideoWriter(video_path, fourcc, 20.0, (screen_width, screen_height))
                        start_time = time.time()
                        while time.time() - start_time < 10:
                            ret, frame = cap.read()
                            if not ret:
                                break
                            frame_resized = cv2.resize(frame, (screen_width, screen_height))
                            out.write(frame_resized)
                            pygame.event.pump()
                        out.release()
                        print("[Karen] Video capture complete. Waiting for audio...")

                        audio_proc.wait()
                        print("[Karen] Audio capture complete. Merging...")

                        # Combine audio + video
                        subprocess.run([
                            "ffmpeg",
                            "-y",  # Overwrite if needed
                            "-i", video_path,
                            "-i", audio_path,
                            "-c:v", "copy",
                            "-c:a", "aac",
                            output_path
                        ])

                        # Clean up separate audio/video files (optional)
                        os.remove(video_path)
                        os.remove(audio_path)

                        print(f"[Karen] Memory saved to: {output_path}")


                    elif "snapshot" in path and current_frame is not None:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"/home/ryn007/Programs/Karen/Recordings/photo_{timestamp}.jpg"
                        cv2.imwrite(filename, current_frame)
                        print(f"[Karen] Snapshot saved: {filename}")

                    elif path.endswith(".sh") or path.endswith(".py"):
                        subprocess.Popen(path, shell=True)
                        print(f"[Karen] Running script: {path}")

                    else:
                        os.system(f"xdg-open '{path}'")



    # Draw scrolling panorama
    viewport = scaled_image.subsurface((scroll_x, 0, screen_width, screen_height))
    screen.blit(viewport, (0, 0))

    # Hover effect
    hover_color = (0, 255, 255, 100)  # Cyan with alpha
    for rect, _ in zones:
        if rect.collidepoint(scroll_x + mouse_x, mouse_y):
            draw_rect = pygame.Rect(rect.x - scroll_x, rect.y, rect.width, rect.height)
            hover_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            hover_surface.fill(hover_color)
            screen.blit(hover_surface, (draw_rect.x, draw_rect.y))

    # Webcam feed
    ret, frame = cap.read()
    current_frame = frame.copy() if ret else None
    
    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (LIVE_FEED_RECT.width, LIVE_FEED_RECT.height))
        frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
        screen.blit(frame_surface, (LIVE_FEED_RECT.x - scroll_x, LIVE_FEED_RECT.y))

    pygame.display.flip()

# Cleanup
cap.release()
pygame.quit()
sys.exit()
