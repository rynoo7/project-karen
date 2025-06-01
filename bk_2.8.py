import pygame
import sys
import os
import time
import sqlite3
import cv2
import numpy as np

class InteractiveZone(pygame.sprite.Sprite):
	def __init__(self, rect, ztype, label=None, db_id=None):
		super().__init__()
		self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
		self.rect = rect
		self.type = ztype
		self.label = label or ztype
		self.db_id = db_id
		self.hovered = False
		self.draw_zone()

	def draw_zone(self):
		self.image.fill((0, 0, 0, 0))  # Fully transparent background
		border_color = (0, 255, 0) if self.hovered else (0, 0, 0, 0)
		pygame.draw.rect(self.image, border_color, self.image.get_rect(), 2)
		font = pygame.font.SysFont(None, 24)
		text = font.render(self.label, True, (255, 255, 255))
		self.image.blit(text, (5, 5))

	def update_hover(self, cursor_rect):
		was_hovered = self.hovered
		self.hovered = self.rect.colliderect(cursor_rect)
		if self.hovered != was_hovered:
			self.draw_zone()

	def on_click(self):
		print(f"[Zone Clicked] Type: {self.type}, Label: {self.label}")

# ... [the rest of the code remains the same until the drawing loop] ...

		zone_x = zone.rect.x - scroll_x
		zone_rect_on_screen = pygame.Rect(zone_x, zone.rect.y, zone.rect.width, zone.rect.height)
		cursor_rect = pygame.Rect(screen_width // 2 - 5, cursor_y - 5, 10, 10)
		zone.update_hover(cursor_rect)

		if zone.type == "live_feed":
			scaled_frame = pygame.transform.scale(frame_surface, (zone.rect.width, zone.rect.height))
			screen.blit(scaled_frame, (zone_x, zone.rect.y))
		screen.blit(zone.image, (zone_x, zone.rect.y))

	else:
		screen.blit(zone.image, (zone_x, zone.rect.y))

# ... [rest of the code remains unchanged] ...
