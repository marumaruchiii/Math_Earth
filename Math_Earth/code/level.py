import pygame 
from settings import *
from pygame.math import Vector2
from tile import Tile
from player import Player, NPC
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI, Inventory
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade, GameOption
from entity import VisibleSprites
from chat import ChatScriptOfPaul, ChatFoodie, ChatReading
from pygame.font import Font

class Level:
	def __init__(self):
		self.game_paused = False
		self.pause_trigger = None
		
		# creating the floor
		self.floor_surf = pygame.image.load('./graphics/tilemap/map_base2.png').convert()

		# sprite group setup
		self.sprs_visible = VisibleSprites(self.floor_surf)
		self.sprs_obstacle = pygame.sprite.Group()

		# attack sprites
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		# sprite setup
		self.active_npc = None
		self.npcs = []
		self.create_map()

		# user interface 
		self.ui = UI()
		self.inventory = Inventory(self.ui)
		self.upgrade = Upgrade(self.player)
		self.game_option = GameOption()

		# particles
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

		# 掉落音效
		self.drop_sound = pygame.mixer.Sound('./audio/put_bag_roughly.mp3')
		self.drop_sound.set_volume(0.5)

		# 掉落書本清單
		self.drop_books = ['book_flame', 'book_Ice1', 'book_Rock1']
		self.reading = ChatReading()
		self.reading_index = None

		# 掉落食物清單
		self.drop_foods = ['food0','food1','food2','food3','food4']
		self.foodie = ChatFoodie()
		self.foodie_index = None

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('./map/fju_map_FloorBlocks.csv'),
			'grass': import_csv_layout('./map/fju_map_Grass.csv'),
			'object': import_csv_layout('./map/fju_map_Objects.csv'),
			'entities': import_csv_layout('./map/fju_map_Entities.csv')
		}
		graphics = {
			'grass': import_folder('./graphics/Grass'),
			'objects': import_folder('./graphics/objects')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.sprs_obstacle],'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile(
								(x,y),
								[self.sprs_visible,self.sprs_obstacle,self.attackable_sprites],
								'grass',
								random_grass_image)

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.sprs_visible,self.sprs_obstacle],'object',surf)

						if style == 'entities':
							if col == '394':
								self.player = Player(
									(x,y),
									[self.sprs_visible],
									self.sprs_obstacle,
									self.create_attack,
									self.destroy_attack,
									self.create_magic,
									self.use_item)
							elif col == '389':
								self.npcs.append( NPC(
									(x,y),
									[self.sprs_visible,self.sprs_obstacle],
									self.sprs_obstacle,
									'paul',
									ChatScriptOfPaul()) )
								npc_center = Vector2(self.npcs[-1].rect.center)
								text_center = npc_center - Vector2(0,40)
								font = Font(UI_FONT,24)
								text_surf = font.render('Paul',True,'Black')
								text_rect = text_surf.get_rect(center=text_center)
								self.floor_surf.blit(text_surf,text_rect)
							else:
								if col == '390': monster_name = 'bamboo' #葉
								elif col == '391': monster_name = 'spirit' #鬼火
								elif col == '392': monster_name ='raccoon' #熊
								elif col == '393': monster_name = 'squid' # axolot 393
								elif col == '395': monster_name ='Cyclope2' #單眼仔
								elif col == '396': monster_name ='bamboo yellow' #黃葉
								else: monster_name = 'squid'
								Enemy(
									monster_name,
									(x,y),
									[self.sprs_visible,self.attackable_sprites],
									self.sprs_obstacle,
									self.damage_player,
									self.trigger_death_particles,
									self.add_exp)

	def create_attack(self):
		
		self.current_attack = Weapon(self.player,[self.sprs_visible,self.attack_sprites])

	def create_magic(self,style,strength,cost):
		if style == 'heal':
			self.magic_player.heal(self.player,strength,cost,[self.sprs_visible])

		if style == 'flame':
			self.magic_player.flame(self.player,cost,[self.sprs_visible,self.attack_sprites])
		
		if style == 'Ice1':
			self.magic_player.Ice1(self.player,cost,[self.sprs_visible,self.attack_sprites])
		
		if style == 'Rock1':
			self.magic_player.Rock1(self.player,cost,[self.sprs_visible,self.attack_sprites])

	def use_item(self):
		pass

	def check_available_npc(self):
		cent_player = Vector2(self.player.rect.center)
		for npc in self.npcs:
			cent_npc = Vector2(npc.rect.center)
			distance_to_npc = cent_player.distance_to(cent_npc)
			if distance_to_npc <= NPC_AVAILABLE_DISTANCE:
				self.active_npc = npc
				return True
		self.active_npc = None
		return False
	
	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def item_drop_logic(self, pos, percent):
		# 書先掉完才會掉食物
		if randint(1,100) <= percent:
			if len(self.drop_books) == 0:
				# 隨機挑選一
				food = choice(self.drop_foods)
				self.animation_player.create_particles('drop',pos,self.sprs_visible)
				self.drop_sound.play()
				self.inventory.get_item(food)
				return
			# 隨機挑選一本書
			book = choice(self.drop_books)
			# 掉落特效
			self.animation_player.create_particles('drop',pos,self.sprs_visible)
			self.animation_player.create_particles(book,pos,self.sprs_visible)
			# 掉落音效
			self.drop_sound.play()
			self.drop_books.remove(book)
			self.inventory.get_item(book)

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0,75)
							for leaf in range(randint(3,6)):
								self.animation_player.create_grass_particles(pos - offset,[self.sprs_visible])
							target_sprite.kill()
							# 20%掉落率
							self.item_drop_logic(pos, 20)
						else:
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	def damage_player(self,amount,attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.sprs_visible])

	def trigger_death_particles(self,pos,particle_type):

		self.animation_player.create_particles(particle_type,pos,self.sprs_visible)

	def add_exp(self,amount):

		self.player.exp += amount

	def check_dialog(self):
		if self.pause_trigger == 'dialog':
			self.active_npc.chat.script_unlock()
			if self.active_npc.chat.first_time:
				return True
		return False

	def toggle_skill_menu(self):
		if self.check_dialog():
			return
		self.pause_trigger = 'skill_menu'
		self.game_paused = not self.game_paused 

	def toggle_game_menu(self):
		if self.check_dialog():
			return
		self.pause_trigger = 'game_menu'
		self.game_paused = not self.game_paused 

	def toggle_dialog(self):
		if self.check_available_npc():
			if self.check_dialog():
				return
			self.pause_trigger = 'dialog'
			self.game_paused = not self.game_paused

	# 吃完食物的效果
	def foodie_start(self, index):
		self.pause_trigger = 'foodie'
		self.foodie_index = index
		self.game_paused = True
		# 吃完回血回魔
		self.player.health += 50
		if self.player.health > self.player.stats['health']:
			self.player.health = self.player.stats['health']
		self.player.energy += 30
		if self.player.energy > self.player.stats['energy']:
			self.player.energy = self.player.stats['energy']

	# 使用書的效果
	def reading_start(self, index):
		self.pause_trigger = 'reading'
		self.reading_index = index
		self.game_paused = True
		# 學到對應的魔法
		self.player.active_magic(index)

	# 對話結束
	def dialog_end(self):
		if self.pause_trigger in ['foodie','reading']:
			self.game_paused = False

	def run(self):
		self.sprs_visible.update_player_movement(self.player)
		self.ui.display(self.player)
		self.inventory.display()

		#檢查Event 因應不同的出不同menu
		if self.game_paused:
			if self.pause_trigger == 'skill_menu':
				self.upgrade.display()
			elif self.pause_trigger == 'game_menu':
				self.game_option.display()
			elif self.pause_trigger == 'dialog':
				item = self.active_npc.dialog()
				if item:
					self.inventory.get_item(item)
			elif self.pause_trigger == 'foodie':
				self.foodie.show_dialog(self.foodie_index)
			elif self.pause_trigger == 'reading':
				self.reading.show_dialog(self.reading_index)
		else:
			self.sprs_visible.update()
			self.sprs_visible.enemy_update(self.player)
			self.player_attack_logic()