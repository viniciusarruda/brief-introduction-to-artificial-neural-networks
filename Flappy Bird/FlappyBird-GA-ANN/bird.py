import pygame as pg
import numpy as np

import random 
class Bird:

	_BIRD_COUNT = 0
	_GRAVITY = 5
	_N_INPUTS = 2
	_N_HIDDEN_NEURONS = 6
	_THRESHOLD = _N_HIDDEN_NEURONS / 2.

	def __init__(self, _brain = None):

		self.bird_num = Bird._BIRD_COUNT
		Bird._BIRD_COUNT += 1
		self.bird = pg.Rect(65, 50, 50, 50)
		self.fitness = 0.0
		self.restart()
		self.brain = _brain if _brain is not None else np.random.rand(Bird._N_INPUTS + 1, Bird._N_HIDDEN_NEURONS) * 2 - 1


	def restart(self):

		self.birdY = 350
		self.jump = self.sprite = self.dist_wall = self.dist_middle = 0
		self.dead = self.out_of_screen = False
		self.jumpSpeed = 10
		self.gravity = Bird._GRAVITY
		self.current_traveled_distance = None
		self.final_speed = None


	def flapOrNot(self):

		if not self.dead:
			inputs = np.array([[self.dist_wall], [self.dist_middle]])
			tmp = self.brain[:-1].transpose().dot(inputs)
			output_hidden_layer = np.heaviside(tmp, 1.)
			tmp = self.brain[-1].transpose().dot(output_hidden_layer)
			output = np.heaviside(tmp, 1.)
			flap = output == 1.

			if (flap):
				self.jump = 17
				self.gravity = Bird._GRAVITY
				self.jumpSpeed = 10


	def render(self):

		hold_sprite = None

		if not self.out_of_screen:

			if self.dead:
				hold_sprite = self.sprite = 2
			elif self.jump:
				hold_sprite = self.sprite = 1
			else:
				hold_sprite = self.sprite
			
			if not self.dead:
				self.sprite = 0

		return hold_sprite, self.birdY


	def update(self, upRect, downRect, middle_wall_x, middle_gap_y, travelled_dist, speed, generation):

		if self.jump:
			self.jumpSpeed -= 1
			self.birdY -= self.jumpSpeed
			self.jump -= 1
		else:
			self.birdY += self.gravity
			self.gravity += 1
		self.bird[1] = self.birdY

		if not self.dead:

			self.dist_wall = middle_wall_x - self.bird[0] - 40
			self.dist_middle = middle_gap_y - self.bird[1]
			self.current_traveled_distance = travelled_dist

			if upRect.colliderect(self.bird) or downRect.colliderect(self.bird):
				self.dead = True
				self.final_speed = speed
				self.fitness += self.current_traveled_distance + generation * self.bird_num # for the first generation is not fair
			
			if not 0 < self.bird[1] < 720:
				self.dead = True
				self.final_speed = speed
				self.out_of_screen = True
				self.fitness += self.current_traveled_distance + generation * self.bird_num # for the first generation is not fair

		elif not 0 < self.bird[1] < 720:
			self.out_of_screen = True



