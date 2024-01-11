import pygame
from sys import exit
from pygame.font import Font
from moviepy.editor import VideoFileClip
from settings import * 

class UI:
	def __init__(self):
		
		# general 
		self.layer = pygame.display.get_surface()
		self.ui_font = Font(UI_FONT,UI_FONT_SIZE)

		# bar setup 
		self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

		# convert weapon dictionary
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)

		# convert magic dictionary
		self.magic_graphics = []
		for magic in magic_data.values():
			magic = pygame.image.load(magic['graphic']).convert_alpha()
			self.magic_graphics.append(magic)

		# convert item dictionary
		self.item_graphics = []
		for item in item_data.values():
			item = pygame.image.load(item['graphic']).convert_alpha()
			self.item_graphics.append(item)

	def show_bar(self,current,max_amount,bg_rect,color):
		# draw bg 
		pygame.draw.rect(self.layer,UI_BG_COLOR,bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		# drawing the bar
		pygame.draw.rect(self.layer,color,current_rect)
		pygame.draw.rect(self.layer,UI_BORDER_COLOR,bg_rect,3)

	def show_exp(self,exp):
		text_surf = self.ui_font.render(str(int(exp)),False,TEXT_COLOR)
		x = self.layer.get_size()[0] - 20
		y = self.layer.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))

		pygame.draw.rect(self.layer,UI_BG_COLOR,text_rect.inflate(20,20))
		self.layer.blit(text_surf,text_rect)
		pygame.draw.rect(self.layer,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

	def show_dialog(self, text, npc_icon):
		x = 0
		y = self.layer.get_size()[1] - 180
		w = self.layer.get_size()[0]
		h = 180
		thick = 5
		bg_rect = pygame.Rect(x,y,w,h)
		pygame.draw.rect(self.layer,UI_BG_COLOR,bg_rect)
		pygame.draw.rect(self.layer,UI_BORDER_COLOR,bg_rect.inflate(thick,thick),thick)

		icon_rect = npc_icon.get_rect(topleft=(x+20,y+20))
		self.layer.blit(npc_icon,icon_rect)

		text_surf = self.ui_font.render(text,False,TEXT_COLOR)
		text_rect = text_surf.get_rect(topleft=(x+100,y+20))
		self.layer.blit(text_surf,text_rect)

	def selection_box(self,left,top, has_switched):
		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pygame.draw.rect(self.layer,UI_BG_COLOR,bg_rect)
		if has_switched:
			pygame.draw.rect(self.layer,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pygame.draw.rect(self.layer,UI_BORDER_COLOR,bg_rect,3)
		return bg_rect

	def weapon_hud(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,630,has_switched)
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.layer.blit(weapon_surf,weapon_rect)

	def magic_hud(self,magic_index,has_switched):
		bg_rect = self.selection_box(90,630,has_switched)
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center = bg_rect.center)

		self.layer.blit(magic_surf,magic_rect)

	#Item 0-9 各自存
	def item_hud(self,item_index,has_switched):
		if item_index == 0:
			bg_rect = self.selection_box(222,630,has_switched)
		if item_index == 1:
			bg_rect = self.selection_box(306,630,has_switched)
		if item_index == 2:
			bg_rect = self.selection_box(390,630,has_switched)
		if item_index == 3:
			bg_rect = self.selection_box(474,630,has_switched)
		if item_index == 4:
			bg_rect = self.selection_box(558,630,has_switched)
		if item_index == 5:
			bg_rect = self.selection_box(642,630,has_switched)
		if item_index == 6:
			bg_rect = self.selection_box(726,630,has_switched)
		if item_index == 7:
			bg_rect = self.selection_box(810,630,has_switched)
		if item_index == 8:
			bg_rect = self.selection_box(894,630,has_switched)
		if item_index == 9:
			bg_rect = self.selection_box(978,630,has_switched)
			
		item_surf = self.item_graphics[item_index]
		item_rect = item_surf.get_rect(center = bg_rect.center)

		self.layer.blit(item_surf,item_rect)

	def display(self,player):
		self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
		self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

		self.show_exp(player.exp)

		self.weapon_hud(player.weapon_index,not player.can_switch_weapon)
		self.magic_hud(player.magic_index,not player.can_switch_magic)
		for i in range(10):
			self.item_hud(i,not player.can_switch_item)
class GameStartMenu:
	def __init__(self, window, clock) -> None:
		self.window = window
		self.clock = clock
		self.clip = VideoFileClip('./video/opening.mp4')

		# ui general 
		self.layer = pygame.display.get_surface()
		self.ui_font = Font(UI_FONT,UI_FONT_SIZE)

		# POSTER底圖
		self.background_art = pygame.image.load('./graphics/game_start/POSTER.png').convert()

	def play_opening_video(self):
		self.clip.preview()

	def enter_start_menu(self):
		run = True
		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						run = False

			self.layer.blit(self.background_art, (0,0))
			pygame.display.update()
			self.clock.tick(FPS)
		pass