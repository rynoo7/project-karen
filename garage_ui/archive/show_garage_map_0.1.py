import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Get screen resolution
info = pygame.display.Info()
width, height = info.current_w, info.current_h

# Create fullscreen window
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Karen's Garage Map")

# Load and scale image
image_path = "/home/ryn007/Programs/Karen/Photos/GARAGE.jpg"
background = pygame.image.load(image_path)
background = pygame.transform.scale(background, (width, height))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(background, (0, 0))
    pygame.display.flip()


pygame.quit()
sys.exit()
