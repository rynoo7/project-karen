import pygame
import sys
import os
import cv2
import time
import subprocess
from datetime import datetime
import threading
from tkinter import Tk, simpledialog

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
        target_fps = 20.0
        interval = 1.0 / target_fps
        next_frame_time = time.time()

        while self.running and (time.time() - self.start_time) < self.duration:
            now = time.time()
            if current_frame is not None and now >= next_frame_time:
                frame_resized = cv2.resize(current_frame, (self.width, self.height))
                self.out.write(frame_resized)
                next_frame_time += interval
            else:
                time.sleep(0.005)

        self.out.release()
        print(f"[Karen] Video saved: {self.output_path}")

# Initialize Pygame and OpenCV
pygame.init()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Karen's Living Memory")

image_path = "/home/ryn007/Programs/Karen/Photos/GARAGE.jpg"
background = pygame.image.load(image_path).convert()
img_width, img_height = background.get_size()
scale_factor = screen_height / img_height
scaled_width = int(img_width * scale_factor)
scaled_image = pygame.transform.scale(background, (scaled_width, screen_height))

scroll_x = 0
max_scroll_x = scaled_width - screen_width
LIVE_FEED_RECT = pygame.Rect(4295, 380, 355, 220)

zones = []
zones.append({"rect": pygame.Rect(3498, 647, 260, 400), "type": "photo", "path": "/home/ryn007/Programs/Karen/Photos/Mobile_toolbox.jpg"})
zones.append({"rect": pygame.Rect(4376, 670, 185, 265), "type": "photo", "path": "/home/ryn007/Programs/Karen/Photos/Karen.jpg"})
zones.append({"rect": pygame.Rect(4415, 320, 115, 60), "type": "snapshot"})
zones.append({"rect": pygame.Rect(4300, 390, 350, 200), "type": "record_video"})
zones.append({"rect": pygame.Rect(4705, 20, 760, 1050), "type": "pdf", "path": "/home/ryn007/Projects/Golf_Cart_Project/Golf_Cart_Motor_Controller_Overview.pdf"})
zones.append({"rect": pygame.Rect(3232, 868, 218, 17), "type": "photo", "path": "/home/ryn007/Programs/Karen/Photos/active_projects_box.jpg"})
zones.append({"rect": pygame.Rect(3188, 550, 280, 150), "type": "photo", "path": "/home/ryn007/Programs/Karen/Photos/BallBearing_toolbox.jpg"})
zones.append({"rect": pygame.Rect(2800, 530, 395, 230), "type": "photo", "path": "/home/ryn007/Programs/Karen/Photos/Mongoose_toolbox.jpg"})
zones.append({"rect": pygame.Rect(1970, 490, 530, 450), "type": "photo", "path": "/home/ryn007/Programs/Karen/Photos/Paint_shelf.jpg"})
zones.append({"rect": pygame.Rect(145, 612, 185, 270), "type": "photo", "path": "/home/ryn007/Programs/Karen/Photos/Eileen.jpg"})
zones.append({"rect": pygame.Rect(4000, 300, 300, 200), "type": "play_video", "path": "/home/ryn007/Videos/SpongeBob.mp4"})
zones.append({"rect": pygame.Rect(4306, 283, 95, 94), "type": "start_recording"})
zones.append({"rect": pygame.Rect(4547, 283, 113, 99), "type": "stop_recording"})

current_frame = None
playing_video = False
video_cap = None

Tk().withdraw()  # Hide tkinter root window

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
            for zone in zones:
                rect = zone["rect"]
                if rect.collidepoint(image_x, image_y):
                    ztype = zone.get("type")
                    path = zone.get("path", "")

                    if ztype == "photo" or ztype == "pdf":
                        os.system(f"xdg-open '{path}'")
                    elif ztype == "snapshot" and current_frame is not None:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"/home/ryn007/Programs/Karen/Recordings/photo_{timestamp}.jpg"
                        cv2.imwrite(filename, current_frame)
                        print(f"[Karen] Snapshot saved: {filename}")
                    elif ztype == "record_video":
                        print("[Karen] Ready to record with button presses.")
                    elif ztype == "play_video":
                        print(f"[Karen] Playing video: {path}")
                        video_cap = cv2.VideoCapture(path)
                        playing_video = True
                    elif ztype == "start_recording":
                        print("[Karen] Starting video recording...")
                        recording = True
                        recording_start_time = time.time()
                        recorded_frames = []
                    elif ztype == "stop_recording":
                        print("[Karen] Stopping recording and saving...")
                        recording = False
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        name = simpledialog.askstring("Save Video", "Enter a name for this video:")
                        if name:
                            filename = f"/home/ryn007/Programs/Karen/Recordings/{name}.mp4"
                        else:
                            filename = f"/home/ryn007/Programs/Karen/Recordings/karen_memory_{timestamp}.mp4"
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        out = cv2.VideoWriter(filename, fourcc, 20.0, (screen_width, screen_height))
                        for frame in recorded_frames:
                            out.write(frame)
                        out.release()
                        print(f"[Karen] Saved recording as: {filename}")

    viewport = scaled_image.subsurface((scroll_x, 0, screen_width, screen_height))
    screen.blit(viewport, (0, 0))

    hover_color = (0, 255, 255, 100)
    for zone in zones:
        rect = zone["rect"]
        if rect.collidepoint(scroll_x + mouse_x, mouse_y):
            draw_rect = pygame.Rect(rect.x - scroll_x, rect.y, rect.width, rect.height)
            hover_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            hover_surface.fill(hover_color)
            screen.blit(hover_surface, (draw_rect.x, draw_rect.y))

    draw_x = LIVE_FEED_RECT.x - scroll_x
    draw_y = LIVE_FEED_RECT.y

    if playing_video and video_cap is not None:
        success, vid_frame = video_cap.read()
        if success:
            fps = video_cap.get(cv2.CAP_PROP_FPS) or 30
            vid_frame = cv2.resize(vid_frame, (LIVE_FEED_RECT.width, LIVE_FEED_RECT.height))
            vid_frame = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB)
            vid_surface = pygame.image.frombuffer(vid_frame.tobytes(), vid_frame.shape[1::-1], "RGB")
            screen.blit(vid_surface, (draw_x, draw_y))
            time.sleep(1 / fps)
        else:
            print("[Karen] Finished playing video.")
            playing_video = False
            video_cap.release()
            video_cap = None
    else:
        ret, frame = cap.read()
        current_frame = frame.copy() if ret else None
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (LIVE_FEED_RECT.width, LIVE_FEED_RECT.height))
            frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
            screen.blit(frame_surface, (draw_x, draw_y))

        if 'recording' in locals() and recording:
            recorded_frames.append(cv2.resize(current_frame, (screen_width, screen_height)))

    pygame.display.flip()

cap.release()
pygame.quit()
sys.exit()
