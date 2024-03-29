import pygame
from settings import *
from random import randint

class MagicPlayer:
	def __init__(self,animation_player):
		self.animation_player = animation_player
		self.sounds = {
		'heal': pygame.mixer.Sound('./audio/heal.wav'),
		'flame':pygame.mixer.Sound('./audio/Fire.wav'),
		'Ice1':pygame.mixer.Sound('./audio/attack/claw.wav'),
		'Rock1':pygame.mixer.Sound('./audio/rock.wav'),
		}
		self.sounds['heal'].set_volume(0.25)
		self.sounds['flame'].set_volume(0.2)
		self.sounds['Ice1'].set_volume(0.2)
		self.sounds['Rock1'].set_volume(0.1)

	def heal(self,player,strength,cost,groups):
		if player.energy >= cost:
			self.sounds['heal'].play()
			player.health += strength
			player.energy -= cost
			if player.health >= player.stats['health']:
				player.health = player.stats['health']
			self.animation_player.create_particles('aura',player.rect.center,groups)
			self.animation_player.create_particles('heal',player.rect.center,groups)

	def flame(self,player,cost,groups):
		if player.energy >= cost:
			player.energy -= cost
			self.sounds['flame'].play()

			if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
			elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
			elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0,-1)
			else: direction = pygame.math.Vector2(0,1)
			#火魔射程7格
			for i in range(1,8):
				if direction.x: #horizontal
					offset_x = (direction.x * i) * TILESIZE
					x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
					y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
					self.animation_player.create_particles('flame',(x,y),groups)
				else: # vertical
					offset_y = (direction.y * i) * TILESIZE
					x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
					y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
					self.animation_player.create_particles('flame',(x,y),groups)

	def Ice1(self,player,cost,groups):
		if player.energy >= cost:
			player.energy -= cost
			self.sounds['Ice1'].play()

			if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
			elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
			elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0,-1)
			else: direction = pygame.math.Vector2(0,1)
			#冰魔射程5格
			for i in range(1,6):
				if direction.x: #horizontal
					offset_x = (direction.x * i) * TILESIZE
					x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
					y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
					self.animation_player.create_particles('Ice1',(x,y),groups)
				else: # vertical
					offset_y = (direction.y * i) * TILESIZE
					x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
					y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
					self.animation_player.create_particles('Ice1',(x,y),groups)
	def Rock1(self,player,cost,groups):
		if player.energy >= cost:
			player.energy -= cost
			self.sounds['Rock1'].play()

			if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
			elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
			elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0,-1)
			else: direction = pygame.math.Vector2(0,1)

			#土魔射程比其他短很多只有3格 但高攻 高MP expense
			for i in range(1,4):
				if direction.x: #horizontal
					offset_x = (direction.x * i) * TILESIZE
					x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
					y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
					self.animation_player.create_particles('Rock1',(x,y),groups)
				else: # vertical
					offset_y = (direction.y * i) * TILESIZE
					x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
					y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
					self.animation_player.create_particles('Rock1',(x,y),groups)