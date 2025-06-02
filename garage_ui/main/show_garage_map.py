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

# Define interactive zones
zones = [
    (pygame.Rect(3498, 647, 260, 400), "/home/ryn007/Programs/Karen/Photos/Mobile_toolbox.jpg"),
    (pygame.Rect(4284, 372, 325, 675), "/home/ryn007/Programs/Karen/Photos/Karen.jpg"),
    
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
