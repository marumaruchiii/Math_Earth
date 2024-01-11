import pygame, sys
from settings import *
from level import Level
from debug import debug

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('數學救地球')
		self.clock = pygame.time.Clock()

		self.level = Level()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.level.toggle_game_menu()
					if event.key == pygame.K_m:
						self.level.toggle_skill_menu()
					if event.key == pygame.K_f:
						self.level.toggle_dialogue()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()