import pygame
from sys import exit
from pygame.font import Font
from pygame.transform import scale, flip
from pygame import Rect
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

	def selection_box(self,left,top, has_switched, text):
		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pygame.draw.rect(self.layer,UI_BG_COLOR,bg_rect)
		if has_switched:
			pygame.draw.rect(self.layer,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pygame.draw.rect(self.layer,UI_BORDER_COLOR,bg_rect,3)
		# 印出按鍵提示
		text_surf = self.ui_font.render(text,True,'White')
		text_rect = text_surf.get_rect(topleft=(left+5,top+5))
		self.layer.blit(text_surf,text_rect)
		return bg_rect

	def weapon_hud(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,630,has_switched, 'Q')
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.layer.blit(weapon_surf,weapon_rect)

	def magic_hud(self,magic_index,has_switched):
		bg_rect = self.selection_box(90,630,has_switched, 'E')
		if magic_index != None:
			magic_surf = self.magic_graphics[magic_index]
			magic_rect = magic_surf.get_rect(center = bg_rect.center)

			self.layer.blit(magic_surf,magic_rect)

	def display(self,player):
		self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
		self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

		self.show_exp(player.exp)

		self.weapon_hud(player.weapon_index,not player.can_switch_weapon)
		self.magic_hud(player.magic_index,not player.can_switch_magic)

class Inventory:
	def __init__(self, ui) -> None:
		self.ui = ui
		self.item_in_bag = []

		# 載入物品圖片
		self.item_graphics = {}
		for key in item_data.keys():
			image = pygame.image.load(item_data[key]['graphic']).convert_alpha()
			self.item_graphics.update({key:image})

	# 玩家使用物品
	def use_item(self,index):
		if index < len(self.item_in_bag):
			key = self.item_in_bag.pop(index)
			return key
		return None

	# 玩家得到物品
	def get_item(self,item):
		if item in self.item_graphics.keys():
			self.item_in_bag.append(item)

	# 顯示物品圖片
	def item_hud(self,rect,item):
		item_surf = self.item_graphics[item]
		item_rect = item_surf.get_rect(center = rect.center)
		self.ui.layer.blit(item_surf,item_rect)

	#Item 0-9 各自存
	def display(self):
		bg_rect = self.ui.selection_box(222,630,False, '1')
		if 0 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[0])
		bg_rect = self.ui.selection_box(306,630,False, '2')
		if 1 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[1])
		bg_rect = self.ui.selection_box(390,630,False, '3')
		if 2 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[2])
		bg_rect = self.ui.selection_box(474,630,False, '4')
		if 3 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[3])
		bg_rect = self.ui.selection_box(558,630,False, '5')
		if 4 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[4])
		bg_rect = self.ui.selection_box(642,630,False, '6')
		if 5 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[5])
		bg_rect = self.ui.selection_box(726,630,False, '7')
		if 6 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[6])
		bg_rect = self.ui.selection_box(810,630,False, '8')
		if 7 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[7])
		bg_rect = self.ui.selection_box(894,630,False, '9')
		if 8 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[8])
		bg_rect = self.ui.selection_box(978,630,False, '0')
		if 9 < len(self.item_in_bag):
			self.item_hud(bg_rect, self.item_in_bag[9])

class GameStartMenu:
	def __init__(self, window, clock) -> None:
		self.window = window
		self.clock = clock
		self.active_button_index = 0
		# x 0-698 y 340-720
		self.buttons = {
			'Game Start':(349, 450),
			'Options':(349, 530),
			'Exit':(349, 610),
		}

		# OP 片頭
		self.clip = VideoFileClip('./video/opening.mp4')


		# ui general 
		self.layer = pygame.display.get_surface()
		self.ui_font = Font(UI_FONT,UI_FONT_SIZE)
		self.menu_font = Font(UI_FONT, MENU_FONT_SIZE)

		# POSTER底圖
		self.background_art = pygame.image.load('./graphics/game_start/POSTER.png').convert()
		self.update_menu_text(self.background_art)
		

		#指標 (三角形)
		self.img_cursor = pygame.image.load('./graphics/game_start/tri.png').convert_alpha()
		self.img_cursor = scale(self.img_cursor, (ITEM_BOX_SIZE//2,ITEM_BOX_SIZE//2))
		self.img_cursor = flip(self.img_cursor, True, False)

		self.cursor_sound = pygame.mixer.Sound('./audio/Menu2.wav')
		self.cursor_sound.set_volume(0.3)

		# 按鍵操作說明
		self.key_map = pygame.image.load('./graphics/test/control.png').convert_alpha()

	def play_opening_video(self):
		self.clip.preview()
		self.clip.close()

	def draw_text(self, text, pos, surf):
		text_surf = self.menu_font.render(text,False,TEXT_COLOR)
		text_rect = text_surf.get_rect(center=pos)
		surf.blit(text_surf,text_rect)

	def update_menu_text(self, surf):
		for key in self.buttons.keys():
			self.draw_text(key, self.buttons[key], surf)

	def draw_cursor(self, index, surf):
		key_list = list(self.buttons.keys())
		key = key_list[index]
		pos_y = self.buttons[key][1]
		cur_rect = self.img_cursor.get_rect(center=(160, pos_y))
		surf.blit(self.img_cursor,cur_rect)

	def get_active_button(self, is_down):
		self.cursor_sound.play()
		if is_down:
			self.active_button_index += 1
		else:
			self.active_button_index -= 1
		#防止button Out of Range
		num = len(self.buttons.keys())
		if self.active_button_index < 0:
			self.active_button_index += num
		if self.active_button_index >= num:
			self.active_button_index -= num

	def enter_start_menu(self):
		self.gameStart_sound = pygame.mixer.Sound('./audio/MATH_EARTH_CV_AI.wav')
		self.gameStartBGM_sound = pygame.mixer.Sound('./audio/Gamestart_BGM.ogg')
		self.gameStart_sound.set_volume(0.1)
		self.gameStartBGM_sound.set_volume(0.1)
		self.gameStart_sound.play()
		#self.gameStartBGM_sound.play()
		show_key_map = False
		loop = True
		while loop:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
						if self.active_button_index == 0:
							loop = False
						if self.active_button_index == 1:
							show_key_map = not show_key_map
						if self.active_button_index == 2:
							pygame.quit()
							exit()
					if not show_key_map:
						if event.key == pygame.K_UP:
							self.get_active_button(False)
						if event.key == pygame.K_DOWN:
							self.get_active_button(True)

			self.layer.blit(self.background_art, (0,0))
			if show_key_map:
				self.layer.blit(self.key_map, (0,0))
			else:
				self.draw_cursor(self.active_button_index, self.layer)
			pygame.display.update()
			self.clock.tick(FPS)
class SettingScrollBar:
	def __init__(self,l,t,w,h,index,font):
		self.rect = pygame.Rect(l,t,w,h)
		self.index = index
		self.ui_font = font

	def display_names(self,surface,name,cost,selected):
		color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

		# title
		title_surf = self.ui_font.render(name,False,color)
		title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

		# cost 
		cost_surf = self.ui_font.render(f'{int(cost)}',False,color)
		cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

		# draw 
		surface.blit(title_surf,title_rect)
		surface.blit(cost_surf,cost_rect)

	def display_bar(self,surface,value,max_value,selected):

		# drawing setup
		top = self.rect.midtop + pygame.math.Vector2(0,60)
		bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
		color = BAR_COLOR_SELECTED if selected else BAR_COLOR

		# bar setup
		full_height = bottom[1] - top[1]
		relative_number = (value / max_value) * full_height
		value_rect = pygame.Rect(top[0] - 15,bottom[1] - relative_number,30,10)

		# draw elements
		pygame.draw.line(surface,color,top,bottom,5)
		pygame.draw.rect(surface,color,value_rect)

	def player_status_setting(self,player):
		upgrade_attribute = list(player.stats.keys())[self.index]

		if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
			player.exp -= player.upgrade_cost[upgrade_attribute]
			player.stats[upgrade_attribute] *= 1.2
			player.upgrade_cost[upgrade_attribute] *= 1.4

		if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
			player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

	def display(self,surface,selection_num,name,value,max_value,cost):
		if self.index == selection_num:
			pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
			pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
		else:
			pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
			pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
	
		self.display_names(surface,name,cost,self.index == selection_num)
		self.display_bar(surface,value,max_value,self.index == selection_num)