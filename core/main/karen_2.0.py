import pygame
import sys
import os
import time

class InteractiveZone(pygame.sprite.Sprite):
	def __init__(self, rect, ztype, path=None, label=None):
		super().__init__()
		self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
		self.rect = rect
		self.type = ztype
		self.path = path
		self.label = label or ztype
		self.draw_zone()

	def draw_zone(self):
		self.image.fill((50, 150, 250, 100))
		font = pygame.font.SysFont(None, 24)
		text = font.render(self.label, True, (255, 255, 255))
		self.image.blit(text, (5, 5))

	def on_click(self):
		if self.type == "photo":
			os.system(f"xdg-open '{self.path}'")
		elif self.type == "add_tool":
			print("[Karen] Add tool clicked")
		elif self.type == "search_tool":
			print("[Karen] Search tool clicked")

pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Karen 2.0")

image_path = "/home/ryn007/Programs/Karen/Photos/GARAGE.jpg"
background = pygame.image.load(image_path).convert()
img_width, img_height = background.get_size()
scale_factor = screen_height / img_height
scaled_width = int(img_width * scale_factor)
scaled_image = pygame.transform.scale(background, (scaled_width, screen_height))

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

zones = pygame.sprite.Group()
scroll_x = 0
adding_zone = False
zone_start = None

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		elif event.type == pygame.MOUSEMOTION:
			dx = event.rel[0]
			if not adding_zone:
				scroll_x += dx
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 2:
				adding_zone = not adding_zone
				if adding_zone:
					zone_start = pygame.mouse.get_pos()
				else:
					zone_end = pygame.mouse.get_pos()
					sx = scroll_x + zone_start[0]
					ex = scroll_x + zone_end[0]
					y1, y2 = zone_start[1], zone_end[1]
					x1, x2 = min(sx, ex), max(sx, ex)
					y1, y2 = min(y1, y2), max(y1, y2)
					new_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
					zones.add(InteractiveZone(new_rect, "custom", label="Zone"))

	scroll_x %= scaled_width
	x1 = -scroll_x
	x2 = x1 + scaled_width
	screen.blit(scaled_image, (x1, 0))
	screen.blit(scaled_image, (x2, 0))

	for zone in zones:
		draw_rect = pygame.Rect(zone.rect.x - scroll_x, zone.rect.y, zone.rect.width, zone.rect.height)
		zone.rect = draw_rect
		screen.blit(zone.image, draw_rect)

	pygame.display.flip()

pygame.quit()
sys.exit()
