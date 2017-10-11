
import pygame as pg
import sys
from random import randint
import numpy as np
import time
import datetime

class FlappyBird:

	_BASE_SPEED = 3
	_MAX_SPEED = 15
	_MIN_OFFSET = -120
	_MAX_OFFSET = 270
	_GAP = 125
	_WALLX = 400  
	_TRAIN_TIME = 10
	_STAT_WIDTH = 400
	_GREEN = (0, 200, 0)
	_RED = (200, 0, 0)
	_WHITE = (255, 255, 255)
	_YELLOW = (200, 200, 0)
	_BLACK = (0, 0, 0)

	def __init__(self):

		pg.init()
		self.current_speed = self.start_time = self.wallx = self.offset = self.upRect = self.downRect = self.middle_wall_x = self.middle_gap_y = self.travelled_dist = self.height = None
		self.start_global_time = time.time()
		self.font = pg.font.SysFont("arial", 18)
		self.new_line = self.font.render("A", True, FlappyBird._BLACK).get_height()
		self.vertical_space = self.new_line / 4
		self.screen = pg.display.set_mode((400 + FlappyBird._STAT_WIDTH, 708))
		self.background = pg.image.load("assets/background.png").convert()
		self.birdSprites = [pg.image.load("assets/1.png").convert_alpha(),
							pg.image.load("assets/2.png").convert_alpha(),
							pg.image.load("assets/dead.png")]
		self.wallUp = pg.image.load("assets/bottom.png").convert_alpha()
		self.wallDown = pg.image.load("assets/top.png").convert_alpha()


	def _updateWalls(self):

		self.wallx -= self.current_speed
		if self.wallx < -100:
			self.wallx = FlappyBird._WALLX
			self.offset = randint(FlappyBird._MIN_OFFSET, FlappyBird._MAX_OFFSET)

		self.upRect = pg.Rect(self.wallx, 360 + FlappyBird._GAP - self.offset + 10, self.wallUp.get_width() - 10, self.wallUp.get_height())
		self.downRect = pg.Rect(self.wallx, 0 - FlappyBird._GAP - self.offset - 10, self.wallDown.get_width() - 10, self.wallDown.get_height())
		self.middle_wall_x = self.wallx + self.wallUp.get_width() / 2.0
		self.middle_gap_y = self.wallDown.get_height() + (FlappyBird._GAP - 7) / 2.0 - FlappyBird._GAP - self.offset


	def run(self, bird, best, best_speed):

		clock = pg.time.Clock()
		self.travelled_dist = 0.
		self.current_speed = FlappyBird._BASE_SPEED
		self.start_time = time.time()
		self.wallx = FlappyBird._WALLX
		self.offset = randint(FlappyBird._MIN_OFFSET, FlappyBird._MAX_OFFSET)
		bias = FlappyBird._TRAIN_TIME

		while True:

			clock.tick(60)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					sys.exit()
				if (event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN):
					bird.flap()

			if self.current_speed < FlappyBird._MAX_SPEED and time.time() - self.start_time > bias:
				self.current_speed += 1
				bias += FlappyBird._TRAIN_TIME

			self.screen.fill(FlappyBird._WHITE)
			self.screen.blit(self.background, (0, 0))
			self.screen.blit(self.wallUp, (self.wallx, 360 + FlappyBird._GAP - self.offset))
			self.screen.blit(self.wallDown, (self.wallx, 0 - FlappyBird._GAP - self.offset))
			self._show_statistcs(bird, best, best_speed)

			sprite, birdY = bird.render()
			if sprite is not None:
				self.screen.blit(self.birdSprites[sprite], (70, birdY))

			self._updateWalls()

			dist_wall = self.middle_wall_x - bird.bird[0] - 40

			bird.update(self.upRect, self.downRect, self.middle_wall_x, self.middle_gap_y, self.travelled_dist, self.current_speed)

			self.travelled_dist += self.current_speed

			pg.display.update()

			if bird.out_of_screen:
				return self.current_speed


	def _show_statistcs(self, bird, best, best_speed):

		self.height = self.new_line

		def _time_format(start_time):
			hours, rem = divmod(time.time() - start_time, 3600)
			minutes, seconds = divmod(rem, 60)
			return '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours),int(minutes),seconds)

		def _blit(text, color):
			t = self.font.render(text, True, color)
			self.screen.blit(t, (400 + ((FlappyBird._STAT_WIDTH - t.get_width()) / 2), self.height))

		def _show_bird_stat(id, text, text_color, fitness):
			self.height += self.new_line + self.vertical_space
			t1 = self.font.render('{} : '.format(id), True, text_color)
			t2 = self.font.render(text, True, text_color)
			t3 = self.font.render(' : {}'.format(fitness), True, text_color)
			self.screen.blit(t1, (400 + ((FlappyBird._STAT_WIDTH - t1.get_width() - t2.get_width() - t3.get_width()) / 2), self.height))
			self.screen.blit(t2, (400 + ((FlappyBird._STAT_WIDTH + t1.get_width() - t2.get_width() - t3.get_width()) / 2), self.height))
			self.screen.blit(t3, (400 + ((FlappyBird._STAT_WIDTH + t1.get_width() + t2.get_width() - t3.get_width()) / 2), self.height))

		def _show_header(text):
			_blit(text, FlappyBird._WHITE)
			self.height += self.new_line + self.vertical_space + self.vertical_space

		def _show_footer(text):
			self.height += self.new_line + self.vertical_space
			_blit(text, FlappyBird._YELLOW)

		pg.draw.rect(self.screen, FlappyBird._BLACK, (400, 0, FlappyBird._STAT_WIDTH, 708), 0)

		_show_header('TIME PLAYING: {}'.format(_time_format(self.start_global_time)))
		_show_header('CURRENT TIME: {}'.format(_time_format(self.start_time)))
		_show_header('SPEED: {} '.format(self.current_speed))
		
		_blit('BIRD ID : STATE : PERFORMANCE', FlappyBird._WHITE)

		color, text = (FlappyBird._RED, 'DEAD') if bird.dead else (FlappyBird._GREEN, 'ALIVE')
		_show_bird_stat(bird.bird_num, text, color, bird.fitness)

		if best is not None:

			self.height += self.vertical_space
			_show_footer('BEST BIRD')
			_show_footer('ID: {}'.format(best.bird_num))
			_show_footer('SPEED: {}'.format(best_speed))
			_show_footer('PERFORMANCE: {}'.format(best.fitness))

		


