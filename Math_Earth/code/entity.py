import pygame
from math import sin
from pygame.math import Vector2

class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.frame_index = 0
		self.animation_speed = 0.15
		self.direction = Vector2()

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: 
			return 255
		else: 
			return 0

class VisibleSprites(pygame.sprite.Group):
	def __init__(self, floor):
		# general setup 
		super().__init__()
		self.surface = pygame.display.get_surface()
		#螢幕Size 除2 得到中心坐標
		self.center = Vector2(self.surface.get_size()) // 2
		#assign 地圖變數
		self.floor = floor

	def update_surface_with_player_movement(self,player):
		# 玩家坐標 - 畫面中央坐標 = 位移量
		offset = Vector2(player.rect.center) - self.center
		# 得到地圖的位移量 地圖 top left is always (0,0)
		floor_offset_pos = Vector2(0,0) - offset
		# 重畫地圖
		self.surface.blit(self.floor, floor_offset_pos)

		# for sprite in VisibleSprites group from y=0 to y=max
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - offset
			self.surface.blit(sprite.image,offset_pos)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)