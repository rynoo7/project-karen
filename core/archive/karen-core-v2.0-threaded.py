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

zones = [
    (pygame.Rect(3498, 647, 260, 400), "/home/ryn007/Programs/Karen/Photos/Mobile_toolbox.jpg"),
    (pygame.Rect(4376, 670, 185, 265), "/home/ryn007/Programs/Karen/Photos/Karen.jpg"),
    (pygame.Rect(4415, 320, 115, 60), "snapshot"),
    (pygame.Rect(4300, 390, 350, 200), "python3 /home/ryn007/Programs/Karen/record_video_cv.py"),
    (pygame.Rect(4705, 20, 760, 1050), "/home/ryn007/Projects/Golf_Cart_Project/Golf_Cart_Motor_Controller_Overview.pdf"),
    (pygame.Rect(3232, 868, 218, 17), "/home/ryn007/Programs/Karen/Photos/active_projects_box.jpg"),
    (pygame.Rect(3188, 550, 280, 150), "/home/ryn007/Programs/Karen/Photos/BallBearing_toolbox.jpg"),
    (pygame.Rect(2800, 530, 395, 230), "/home/ryn007/Programs/Karen/Photos/Mongoose_toolbox.jpg"),
    (pygame.Rect(1970, 490, 530, 450), "/home/ryn007/Programs/Karen/Photos/Paint_shelf.jpg"),
    (pygame.Rect(145, 612, 185, 270), "/home/ryn007/Programs/Karen/Photos/Eileen.jpg"),
    (pygame.Rect(4000, 300, 300, 200), "play_video:/home/ryn007/Videos/karen_intro.mp4")
]

current_frame = None
playing_video = False
video_cap = None

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
                    if path.startswith("play_video:"):
                        video_path = path.split(":", 1)[1]
                        print(f"[Karen] Playing memory: {video_path}")
                        playing_video = True
                        # Start audio playback in background using ffplay
                        audio_proc = subprocess.Popen(
                            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", video_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )

                        video_cap = cv2.VideoCapture(video_path)

                    elif "record_video" in path:
                        print("[Karen] Starting background video and audio recording...")
                        audio_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        audio_path = f"/home/ryn007/Programs/Karen/Recordings/audio_{audio_timestamp}.wav"

                        audio_proc = subprocess.Popen(
                            ["ffmpeg", "-f", "alsa", "-i", "default", "-t", "10", audio_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )

                        recorder = VideoRecorder(screen_width, screen_height)
                        recorder.start()

                        def merge_after_delay():
                            recorder.join()
                            audio_proc.wait()
                            print("[Karen] Merging audio and video...")
                            merged_path = f"/home/ryn007/Programs/Karen/Recordings/karen_memory_{audio_timestamp}.mp4"
                            subprocess.run([
                                "ffmpeg", "-y",
                                "-i", recorder.output_path,
                                "-i", audio_path,
                                "-c:v", "copy",
                                "-c:a", "aac",
                                merged_path
                            ])
                            os.remove(recorder.output_path)
                            os.remove(audio_path)
                            print(f"[Karen] Memory complete: {merged_path}")

                        threading.Thread(target=merge_after_delay).start()

                    elif path == "snapshot" and current_frame is not None:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"/home/ryn007/Programs/Karen/Recordings/photo_{timestamp}.jpg"
                        cv2.imwrite(filename, current_frame)
                        print(f"[Karen] Snapshot saved: {filename}")
                    elif path.endswith(".sh") or path.endswith(".py"):
                        subprocess.Popen(path, shell=True)
                        print(f"[Karen] Running script: {path}")
                    else:
                        os.system(f"xdg-open '{path}'")

    viewport = scaled_image.subsurface((scroll_x, 0, screen_width, screen_height))
    screen.blit(viewport, (0, 0))

    hover_color = (0, 255, 255, 100)
    for rect, _ in zones:
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
            fps = video_cap.get(cv2.CAP_PROP_FPS) or 30  # fallback to 30 if unknown
            vid_frame = cv2.resize(vid_frame, (LIVE_FEED_RECT.width, LIVE_FEED_RECT.height))
            vid_frame = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB)
            vid_surface = pygame.image.frombuffer(vid_frame.tobytes(), vid_frame.shape[1::-1], "RGB")
            screen.blit(vid_surface, (draw_x, draw_y))
            pygame.display.flip()
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

    pygame.display.flip()

cap.release()
pygame.quit()
sys.exit()
