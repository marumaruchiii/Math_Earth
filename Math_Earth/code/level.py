import pygame 
from settings import *
from tile import Tile
from player import Player, NPC
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade, GameOption
from entity import VisibleSprites

class Level:
	def __init__(self):
		self.game_paused = False
		self.is_game_option = False

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
		self.create_map()

		# user interface 
		self.ui = UI()
		self.upgrade = Upgrade(self.player)
		self.game_option = GameOption()

		# particles
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

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
									self.create_magic)
							elif col == '389':
								self.player = NPC(
									(x,y),
									[self.sprs_visible,self.sprs_obstacle],
									self.sprs_obstacle,
									'paul', floor_surf=self.floor_surf)
							else:
								if col == '390': monster_name = 'bamboo'
								elif col == '391': monster_name = 'spirit' #spirit
								elif col == '392': monster_name ='raccoon'
								elif col == '393': monster_name = 'boxx' #boxx 393
								elif col == '395': monster_name ='Cyclope2'
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

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

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

	def toggle_skill_menu(self):
		self.is_game_option = False
		self.game_paused = not self.game_paused 

	def toggle_game_menu(self):
		self.is_game_option = True
		self.game_paused = not self.game_paused

	def run(self):
			self.sprs_visible.update_player_movement(self.player)
			self.ui.display(self.player)
			
			if self.game_paused:
				if self.is_game_option:
					self.game_option.display()
				else:
					self.upgrade.display()
			else:
				self.sprs_visible.update()
				self.sprs_visible.enemy_update(self.player)
				self.player_attack_logic()