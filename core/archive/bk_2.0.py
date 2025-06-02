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
		if self.type == "photo" and self.path:
			os.system(f"xdg-open '{self.path}'")
		elif self.type == "add_tool":
			print("[Karen] Add Tool Clicked")
		elif self.type == "search_tool":
			print("[Karen] Search Tool Clicked")

class CursorSprite(pygame.sprite.Sprite):
	def __init__(self, screen_width, screen_height):
		super().__init__()
		self.image = pygame.Surface((10, 10))
		self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.rect.centerx = screen_width // 2
		self.rect.centery = screen_height // 2

	def update(self, dy):
		self.rect.centery += dy
		self.rect.centery = max(0, min(self.screen_height, self.rect.centery))

# Initialize Pygame
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

scroll_x = 0

zones = pygame.sprite.Group()
zones.add(InteractiveZone(pygame.Rect(100, 100, 150, 75), "add_tool"))
zones.add(InteractiveZone(pygame.Rect(100, 200, 150, 75), "search_tool"))

cursor = CursorSprite(screen_width, screen_height)
cursor_group = pygame.sprite.Group(cursor)

running = True
while running:
	dy = 0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		elif event.type == pygame.MOUSEMOTION:
			dx, dy = event.rel
			scroll_x += dx
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for zone in zones:
				if cursor.rect.colliderect(zone.rect.move(-scroll_x, 0)):
					zone.on_click()

	scroll_x %= scaled_width

	x1 = -scroll_x
	x2 = x1 + scaled_width
	screen.blit(scaled_image, (x1, 0))
	screen.blit(scaled_image, (x2, 0))

	zones.draw(screen)
	for zone in zones:
		adjusted_rect = zone.rect.move(-scroll_x, 0)
		screen.blit(zone.image, adjusted_rect)

	cursor.update(dy)
	cursor_group.draw(screen)

	pygame.display.flip()

pygame.quit()
sys.exit()
