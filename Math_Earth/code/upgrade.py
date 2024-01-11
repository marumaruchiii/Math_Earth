import pygame
from pygame.font import Font
from settings import *

class Upgrade:
	def __init__(self,player):

		# general setup
		self.layer = pygame.display.get_surface()
		self.player = player
		self.attribute_nr = len(player.stats)
		self.attribute_names = list(player.stats.keys())
		self.max_values = list(player.max_stats.values())
		self.ui_font = Font(UI_FONT, UI_FONT_SIZE)

		# item creation
		self.height = self.layer.get_size()[1] * 0.8
		self.width = self.layer.get_size()[0] // 6
		self.create_items()

		# selection system 
		self.selection_index = 0
		self.selection_time = None
		self.can_move = True

	def input(self):
		keys = pygame.key.get_pressed()

		if self.can_move:
			if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
				self.selection_index += 1
				self.can_move = False
				self.selection_time = pygame.time.get_ticks()
			elif keys[pygame.K_LEFT] and self.selection_index >= 1:
				self.selection_index -= 1
				self.can_move = False
				self.selection_time = pygame.time.get_ticks()

			if keys[pygame.K_SPACE]:
				self.can_move = False
				self.selection_time = pygame.time.get_ticks()
				self.item_list[self.selection_index].player_status_setting(self.player)

	def selection_cooldown(self):
		if not self.can_move:
			current_time = pygame.time.get_ticks()
			if current_time - self.selection_time >= 300:
				self.can_move = True

	def create_items(self):
		self.item_list = []

		for item, index in enumerate(range(self.attribute_nr)):
			# horizontal position
			full_width = self.layer.get_size()[0]
			increment = full_width // self.attribute_nr
			left = (item * increment) + (increment - self.width) // 2
			
			# vertical position 
			top = self.layer.get_size()[1] * 0.1

			# create the object 
			item = SettingScrollBar(left,top,self.width,self.height,index,self.ui_font)
			self.item_list.append(item)

	def display(self):
		self.input()
		self.selection_cooldown()

		for index, item in enumerate(self.item_list):

			# get attributes
			name = self.attribute_names[index]
			value = self.player.get_value_by_index(index)
			max_value = self.max_values[index]
			cost = self.player.get_cost_by_index(index)
			item.display(self.layer,self.selection_index,name,value,max_value,cost)

# 遊戲Menu
class GameOption:
	def __init__(self):
		self.option = { 'music':50, 'audio_effect':50 }
		self.option_max = { 'music':100, 'audio_effect':100 }

		# sound 
		self.main_sound = pygame.mixer.Sound('./audio/main.ogg')
		self.main_sound.set_volume( self.option['music'] / self.option_max['music'] )
		self.main_sound.play(loops = -1)

		# general setup
		self.layer = pygame.display.get_surface()
		self.attribute_nr = len(self.option)
		self.attribute_names = list(self.option.keys())
		self.max_values = list(self.option_max.values())
		self.ui_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

		# menu bar 的小方塊
		self.height = self.layer.get_size()[1] * 0.8
		self.width = self.layer.get_size()[0] // 6
		self.create_items()

		# selection system 
		self.selection_index = 0
		self.selection_time = None
		self.can_move = True

	def create_items(self):
		self.item_list = []

		for item, index in enumerate(range(self.attribute_nr)):
			# horizontal position
			full_width = self.layer.get_size()[0]
			increment = full_width // self.attribute_nr
			left = (item * increment) + (increment - self.width) // 2
			
			# vertical position 
			top = self.layer.get_size()[1] * 0.1

			# create the object 
			item = SettingScrollBar(left,top,self.width,self.height,index,self.ui_font)
			self.item_list.append(item)

	def game_option_setting(self, is_up):
		opt_key = list(self.option.keys())[self.selection_index]
		if is_up:
			self.option[opt_key] += 10
		else:
			self.option[opt_key] -= 10
		self.option[opt_key] = max(self.option[opt_key], 0)
		self.option[opt_key] = min(self.option[opt_key], self.option_max[opt_key])
		self.main_sound.set_volume( self.option['music'] / self.option_max['music'] )

	def input(self):
		keys = pygame.key.get_pressed()

		if self.can_move:
			if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
				self.can_move = False
				self.selection_index += 1
				self.selection_time = pygame.time.get_ticks()
			elif keys[pygame.K_LEFT] and self.selection_index >= 1:
				self.can_move = False
				self.selection_index -= 1
				self.selection_time = pygame.time.get_ticks()

			if keys[pygame.K_UP]:
				self.selection_time = pygame.time.get_ticks()
				self.can_move = False
				self.game_option_setting(True)
			if keys[pygame.K_DOWN]:
				self.selection_time = pygame.time.get_ticks()
				self.can_move = False
				self.game_option_setting(False)

	def selection_cooldown(self):
		if not self.can_move:
			current_time = pygame.time.get_ticks()
			if current_time - self.selection_time >= 300:
				self.can_move = True

	def display(self):
		self.input()
		self.selection_cooldown()

		for index, item in enumerate(self.item_list):
			# get attributes
			name = self.attribute_names[index]
			value = self.option[(list(self.option.keys())[index])]
			max_value = self.max_values[index]
			item.display(self.layer,self.selection_index,name,value,max_value,0)

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