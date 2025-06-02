import pygame
import sys
import os
import cv2

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

running = True
while running:
    mouse_x = pygame.mouse.get_pos()[0]
    scroll_x = int((mouse_x / screen_width) * max_scroll_x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_x, click_y = event.pos
            image_x = scroll_x + click_x
            image_y = click_y
            if pygame.Rect(3498, 647, 260, 400).collidepoint(image_x, image_y):
                os.system("xdg-open /home/ryn007/Programs/Karen/Photos/Mobile_toolbox.jpg")
            if pygame.Rect(4284, 372, 325, 675).collidepoint(image_x, image_y):
                os.system("xdg-open /home/ryn007/Programs/Karen/Photos/Karen.jpg")
            if pygame.Rect(4705, 20, 760, 1050).collidepoint(image_x, image_y):
                os.system("xdg-open /home/ryn007/Programs/Karen/Photos/golfcart.jpg")
            if pygame.Rect(3188, 550, 280, 150).collidepoint(image_x, image_y):
                os.system("xdg-open /home/ryn007/Programs/Karen/Photos/BallBearing_toolbox.jpg")
            if pygame.Rect(2800, 530, 395, 230).collidepoint(image_x, image_y):
                os.system("xdg-open /home/ryn007/Programs/Karen/Photos/Mongoose_toolbox.jpg")
            if pygame.Rect(1970, 490,530, 450).collidepoint(image_x, image_y):
                os.system("xdg-open /home/ryn007/Programs/Karen/Photos/Paint_shelf.jpg")
            if pygame.Rect(145, 612, 185, 270).collidepoint(image_x, image_y):
                os.system("xdg-open /home/ryn007/Programs/Karen/Photos/Eileen.jpg")

    # Draw scrolling panorama
    viewport = scaled_image.subsurface((scroll_x, 0, screen_width, screen_height))
    screen.blit(viewport, (0, 0))

    # Read webcam frame
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)  # Mirror it
        frame = cv2.resize(frame, (LIVE_FEED_RECT.width, LIVE_FEED_RECT.height))
        frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        # Convert to screen coordinates by subtracting scroll_x
        draw_x = LIVE_FEED_RECT.x - scroll_x
        draw_y = LIVE_FEED_RECT.y
        screen.blit(frame_surface, (draw_x, draw_y))

    pygame.display.flip()

# Cleanup
cap.release()
pygame.quit()
sys.exit()
