import pygame
import sys
import os
import time

class InteractiveZone(pygame.sprite.Sprite):
	def __init__(self, rect, ztype, label=None):
		super().__init__()
		self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
		self.rect = rect
		self.type = ztype
		self.label = label or ztype
		self.draw_zone()

	def draw_zone(self):
		self.image.fill((50, 150, 250, 100))
		font = pygame.font.SysFont(None, 24)
		text = font.render(self.label, True, (255, 255, 255))
		self.image.blit(text, (5, 5))

	def on_click(self):
		print(f"[Zone Clicked] Type: {self.type}, Label: {self.label}")

class CursorSprite(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
		pygame.draw.circle(self.image, (255, 0, 0), (5, 5), 5)
		self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))

	def update(self, y_offset):
		y = self.rect.y + y_offset
		y = max(0, min(screen_height - self.rect.height, y))
		self.rect.y = y

# Initialize Pygame
pygame.init()

# Setup screen
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Karen 2.0")

# Load and scale panorama
image_path = "/home/ryn007/Programs/Karen/Photos/GARAGE.jpg"
background = pygame.image.load(image_path).convert()
img_width, img_height = background.get_size()
scale_factor = screen_height / img_height
scaled_width = int(img_width * scale_factor)
scaled_image = pygame.transform.scale(background, (scaled_width, screen_height))

scroll_x = 0
zones = pygame.sprite.Group()
centered_mouse = True
zone_creation_mode = False
zone_start = None
new_zone_rect = None

cursor = CursorSprite()
cursor_group = pygame.sprite.Group(cursor)

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Main loop
running = True
while running:
	mouse_x, mouse_y = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 2:  # Center click to toggle zone creation mode
				zone_creation_mode = not zone_creation_mode
				pygame.mouse.set_visible(zone_creation_mode)
				pygame.event.set_grab(not zone_creation_mode)
				if not zone_creation_mode:
					zone_start = None
			elif event.button == 1 and zone_creation_mode:
				zone_start = (scroll_x + mouse_x, mouse_y)
			elif event.button == 1 and not zone_creation_mode:
				for zone in zones:
					if cursor.rect.colliderect(pygame.Rect(zone.rect.x - scroll_x, zone.rect.y, zone.rect.width, zone.rect.height)):
						zone.on_click()
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1 and zone_creation_mode and zone_start:
				zone_end = (scroll_x + mouse_x, mouse_y)
				x1, y1 = zone_start
				x2, y2 = zone_end
				left, top = min(x1, x2), min(y1, y2)
				width, height = abs(x1 - x2), abs(y1 - y2)
				if width > 5 and height > 5:
					rect = pygame.Rect(left, top, width, height)
					zones.add(InteractiveZone(rect, "custom_zone"))
					print(f"[Karen] Created zone at: {rect}")
				zone_start = None
				zone_creation_mode = False
				pygame.mouse.set_visible(False)
				pygame.event.set_grab(True)
		elif event.type == pygame.MOUSEMOTION and not zone_creation_mode:
			scroll_x += event.rel[0]
			y_motion = event.rel[1]
			cursor.update(y_motion)

	scroll_x %= scaled_width

	x1 = -scroll_x
	x2 = x1 + scaled_width
	screen.blit(scaled_image, (x1, 0))
	screen.blit(scaled_image, (x2, 0))

	for zone in zones:
		screen.blit(zone.image, (zone.rect.x - scroll_x, zone.rect.y))

	if zone_creation_mode and zone_start:
		temp_end = (scroll_x + mouse_x, mouse_y)
		x1, y1 = zone_start
		x2, y2 = temp_end
		left, top = min(x1, x2), min(y1, y2)
		width, height = abs(x1 - x2), abs(y1 - y2)
		preview_rect = pygame.Rect(left - scroll_x, top, width, height)
		pygame.draw.rect(screen, (0, 255, 0), preview_rect, 2)

	cursor_group.draw(screen)
	pygame.display.flip()

pygame.quit()
sys.exit()
