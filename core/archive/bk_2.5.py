import pygame
import sys
import os
import time
import sqlite3

class InteractiveZone(pygame.sprite.Sprite):
	def __init__(self, rect, ztype, label=None, db_id=None):
		super().__init__()
		self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
		self.rect = rect
		self.type = ztype
		self.label = label or ztype
		self.db_id = db_id
		self.draw_zone()

	def draw_zone(self):
		self.image.fill((50, 150, 250, 100))
		font = pygame.font.SysFont(None, 24)
		text = font.render(self.label, True, (255, 255, 255))
		self.image.blit(text, (5, 5))

	def on_click(self):
		print(f"[Zone Clicked] Type: {self.type}, Label: {self.label}")

# Database functions
def connect_db():
	return sqlite3.connect("/home/ryn007/Programs/Karen/garage.db")

def save_zone_to_db(rect, ztype, label):
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute("INSERT INTO zones (x, y, width, height, type, label) VALUES (?, ?, ?, ?, ?, ?)",
				   (rect.x, rect.y, rect.width, rect.height, ztype, label))
	conn.commit()
	zone_id = cursor.lastrowid
	conn.close()
	return zone_id

def delete_zone_from_db(zone_id):
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute("DELETE FROM zones WHERE id = ?", (zone_id,))
	conn.commit()
	conn.close()

def update_zone_in_db(zone_id, ztype, label):
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute("UPDATE zones SET type = ?, label = ? WHERE id = ?", (ztype, label, zone_id))
	conn.commit()
	conn.close()

def load_zones_from_db():
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute("SELECT id, x, y, width, height, type, label FROM zones")
	rows = cursor.fetchall()
	conn.close()
	return [InteractiveZone(pygame.Rect(x, y, w, h), ztype, label, db_id=zone_id)
			for zone_id, x, y, w, h, ztype, label in rows]

class ConfirmationDialog:
	def __init__(self, message):
		self.message = message
		self.font = pygame.font.SysFont(None, 32)
		size = (400, 150)
		self.surface = pygame.Surface(size)
		self.rect = self.surface.get_rect(center=(screen_width // 2, screen_height // 2))
		self.yes_rect = pygame.Rect(self.rect.centerx - 80, self.rect.bottom - 50, 60, 30)
		self.no_rect = pygame.Rect(self.rect.centerx + 20, self.rect.bottom - 50, 60, 30)
		self.result = None

	def draw(self, screen):
		self.surface.fill((30, 30, 30))
		pygame.draw.rect(self.surface, (255, 0, 0), self.yes_rect.move(-self.rect.left, -self.rect.top))
		pygame.draw.rect(self.surface, (0, 255, 0), self.no_rect.move(-self.rect.left, -self.rect.top))
		msg = self.font.render(self.message, True, (255, 255, 255))
		self.surface.blit(msg, (20, 20))
		self.surface.blit(self.font.render("Yes", True, (255, 255, 255)), self.yes_rect.move(-self.rect.left + 10, -self.rect.top))
		self.surface.blit(self.font.render("No", True, (255, 255, 255)), self.no_rect.move(-self.rect.left + 10, -self.rect.top))
		screen.blit(self.surface, self.rect)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.yes_rect.collidepoint(event.pos):
				self.result = True
			elif self.no_rect.collidepoint(event.pos):
				self.result = False

class ZoneEditDialog:
	def __init__(self, zone):
		self.zone = zone
		self.font = pygame.font.SysFont(None, 28)
		self.label_input = zone.label
		self.type_input = zone.type
		self.step = 0
		self.done = False

	def draw(self, screen):
		surface = pygame.Surface((500, 180))
		surface.fill((0, 0, 0))
		surface.set_alpha(240)
		rect = surface.get_rect(center=(screen_width // 2, screen_height // 2))
		text_label = self.font.render("Edit Label: " + self.label_input, True, (255, 255, 255))
		text_type = self.font.render("Edit Type: " + self.type_input, True, (255, 255, 255))
		prompt = self.font.render("Press Enter to switch field, ESC to save", True, (200, 200, 200))
		surface.blit(text_label, (20, 20))
		surface.blit(text_type, (20, 60))
		surface.blit(prompt, (20, 120))
		screen.blit(surface, rect)

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.done = True
			elif event.key == pygame.K_RETURN:
				self.step = (self.step + 1) % 2
			elif event.key == pygame.K_BACKSPACE:
				if self.step == 0:
					self.label_input = self.label_input[:-1]
				else:
					self.type_input = self.type_input[:-1]
			else:
				char = event.unicode
				if char.isprintable():
					if self.step == 0:
						self.label_input += char
					else:
						self.type_input += char

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

scroll_x = 0
zones = pygame.sprite.Group(load_zones_from_db())
centered_mouse = True
zone_creation_mode = False
zone_start = None
new_zone_rect = None
zone_pending_deletion = None
confirm_dialog = None
edit_dialog = None

cursor_sprite = pygame.Surface((10, 10))
cursor_sprite.fill((255, 255, 255))
cursor_y = screen_height // 2

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
pygame.mouse.set_pos((screen_width // 2, screen_height // 2))

running = True
while running:
	mouse_x, mouse_y = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		elif confirm_dialog:
			confirm_dialog.handle_event(event)
		elif edit_dialog:
			edit_dialog.handle_event(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 2:
				zone_creation_mode = not zone_creation_mode
				pygame.mouse.set_visible(zone_creation_mode)
				pygame.event.set_grab(not zone_creation_mode)
				if not zone_creation_mode:
					zone_start = None
			elif event.button == 1 and zone_creation_mode:
				zone_start = (scroll_x + mouse_x, mouse_y)
			elif event.button == 3 and zone_creation_mode:
				for zone in zones:
					if zone.rect.collidepoint(scroll_x + mouse_x, mouse_y):
						zone_pending_deletion = zone
						confirm_dialog = ConfirmationDialog("Delete this zone?")
			elif event.button == 3 and not zone_creation_mode:
				for zone in zones:
					if zone.rect.collidepoint(scroll_x + screen_width // 2, cursor_y):
						edit_dialog = ZoneEditDialog(zone)
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1 and zone_creation_mode and zone_start:
				zone_end = (scroll_x + mouse_x, mouse_y)
				x1, y1 = zone_start
				x2, y2 = zone_end
				left, top = min(x1, x2), min(y1, y2)
				width, height = abs(x1 - x2), abs(y1 - y2)
				if width > 5 and height > 5:
					rect = pygame.Rect(left, top, width, height)
					zone_id = save_zone_to_db(rect, "custom_zone", "custom_zone")
					zones.add(InteractiveZone(rect, "custom_zone", db_id=zone_id))
					print(f"[Karen] Created zone at: {rect}")
				zone_start = None
				zone_creation_mode = False
				pygame.mouse.set_visible(False)
				pygame.event.set_grab(True)
		elif event.type == pygame.MOUSEMOTION and not zone_creation_mode:
			cursor_y += event.rel[1]
			cursor_y = max(0, min(screen_height - 1, cursor_y))
			scroll_x += event.rel[0]

	if confirm_dialog and confirm_dialog.result is not None:
		if confirm_dialog.result and zone_pending_deletion:
			delete_zone_from_db(zone_pending_deletion.db_id)
			zones.remove(zone_pending_deletion)
		zone_pending_deletion = None
		confirm_dialog = None

	if edit_dialog and edit_dialog.done:
		edit_dialog.zone.label = edit_dialog.label_input
		edit_dialog.zone.type = edit_dialog.type_input
		edit_dialog.zone.draw_zone()
		update_zone_in_db(edit_dialog.zone.db_id, edit_dialog.zone.type, edit_dialog.zone.label)
		edit_dialog = None

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

	if confirm_dialog:
		confirm_dialog.draw(screen)
	if edit_dialog:
		edit_dialog.draw(screen)

	screen.blit(cursor_sprite, (screen_width // 2 - 5, cursor_y - 5))
	pygame.display.flip()

pygame.quit()
sys.exit()
