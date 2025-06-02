import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Get screen resolution
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Karen's Garage Panorama")

# Load full-size image
image_path = "/home/ryn007/Programs/Karen/Photos/GARAGE.jpg"
background = pygame.image.load(image_path).convert()

# Get the dimensions of the full image
img_width, img_height = background.get_size()

# Scale the image to fit the screen vertically, but keep full width
scale_factor = screen_height / img_height
scaled_width = int(img_width * scale_factor)
scaled_image = pygame.transform.scale(background, (scaled_width, screen_height))

# Define the toolbox click zone (image coordinates)
TOOLBOX_RECT = pygame.Rect(
    3553, 693,  # X1, Y1 (top-left corner)
    183, 249    # width, height
)

# Scrolling logic
scroll_x = 0
max_scroll_x = scaled_width - screen_width

# Main loop
running = True
while running:
    mouse_x = pygame.mouse.get_pos()[0]
# Print click position in full-image coordinates
    if pygame.mouse.get_pressed()[0]:  # Left mouse click
        click_x, click_y = pygame.mouse.get_pos()
        image_x = scroll_x + click_x
        image_y = click_y
        print(f"Clicked image coordinates: ({image_x}, {image_y})")

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
            if TOOLBOX_RECT.collidepoint(image_x, image_y):
                print("Toolbox clicked! Opening photo...")
                os.system("xdg-open /home/ryn007/Programs/Karen/Photos/Mobile_toolbox.jpg")


    
    # Print click position in full-image coordinates
  #  if pygame.mouse.get_pressed()[0]:  # Left mouse click
  #      click_x, click_y = pygame.mouse.get_pos()
   #     image_x = scroll_x + click_x
   #     image_y = click_y
   #     print(f"Clicked image coordinates: ({image_x}, {image_y})")
    
    scroll_x = int((mouse_x / screen_width) * max_scroll_x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Blit the visible portion of the image
    viewport = scaled_image.subsurface((scroll_x, 0, screen_width, screen_height))
    screen.blit(viewport, (0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()
