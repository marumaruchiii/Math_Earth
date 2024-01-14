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
		self.start_menu.play_opening_video()
		self.start_menu.enter_start_menu()
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
						# 物品使用效果
						if item:
							# 如果用了書 就解鎖魔法
							if item == 'book_heal':
								self.level.reading_start(0)
							if item == 'book_flame':
								self.level.reading_start(1)
							if item == 'book_Ice1':
								self.level.reading_start(2)
							if item == 'book_Rock1':
								self.level.reading_start(3)
							# 判斷是不是food開頭
							if item[:4] == 'food':
								index = int(item[4:])
								self.level.foodie_start(index)
					if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
						self.level.dialog_end()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()