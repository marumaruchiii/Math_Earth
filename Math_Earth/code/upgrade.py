import pygame
from pygame.font import Font
from ui import SettingScrollBar
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
