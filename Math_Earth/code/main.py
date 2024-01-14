import pygame, sys
from settings import *
from ui import GameStartMenu
from level import Level
from debug import debug
from pygame import K_ESCAPE, K_m, K_f, K_f, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('數學救地球')
		self.screen.fill(WATER_COLOR)
		self.clock = pygame.time.Clock()
		self.start_menu = GameStartMenu(self.screen, self.clock)
		self.level = Level()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:
						self.level.toggle_game_menu()
					if event.key == K_m:
						self.level.toggle_skill_menu()
					if event.key == K_f:
						self.level.toggle_dialog()
					if event.key in [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
						# 把key的數字轉成index
						index = event.key - 49 if event.key != 48 else 9
						item = self.level.inventory.use_item(index)
						# 如果用了書 就解鎖魔法
						if item == 'book_heal':  self.level.player.active_magic(0)
						if item == 'book_flame': self.level.player.active_magic(1)
						if item == 'book_Ice1':  self.level.player.active_magic(2)
						if item == 'book_Rock1': self.level.player.active_magic(3)

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.start_menu.play_opening_video()
	game.start_menu.enter_start_menu()
	game.run()