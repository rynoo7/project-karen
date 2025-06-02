import pygame
import sys
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Karen - Zone Creator")

image_path = "/home/ryn007/Programs/Karen/Photos/GARAGE.jpg"
background = pygame.image.load(image_path).convert()
img_width, img_height = background.get_size()
scale_factor = screen_height / img_height
scaled_width = int(img_width * scale_factor)
scaled_image = pygame.transform.scale(background, (scaled_width, screen_height))

scroll_x = 0
max_scroll_x = scaled_width - screen_width

zones = []
drawing = False
start_pos = (0, 0)

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scroll_x = int((mouse_x / screen_width) * max_scroll_x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_s:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"zones_{timestamp}.txt"
                with open(filename, "w") as f:
                    for rect in zones:
                        f.write(f"pygame.Rect({rect.x}, {rect.y}, {rect.width}, {rect.height})\n")
                print(f"[Karen] Zones saved to: {filename}")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = (scroll_x + event.pos[0], event.pos[1])
            elif event.button == 3:
                if zones:
                    zones.pop()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = (scroll_x + event.pos[0], event.pos[1])
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                zones.append(rect)
                drawing = False

    # Draw
    viewport = scaled_image.subsurface((scroll_x, 0, screen_width, screen_height))
    screen.blit(viewport, (0, 0))

    for rect in zones:
        draw_rect = pygame.Rect(rect.x - scroll_x, rect.y, rect.width, rect.height)
        pygame.draw.rect(screen, (0, 255, 0), draw_rect, 2)

    if drawing:
        current_x, current_y = scroll_x + mouse_x, mouse_y
        x1, y1 = start_pos
        x2, y2 = current_x, current_y
        temp_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        draw_temp = pygame.Rect(temp_rect.x - scroll_x, temp_rect.y, temp_rect.width, temp_rect.height)
        pygame.draw.rect(screen, (255, 255, 0), draw_temp, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
