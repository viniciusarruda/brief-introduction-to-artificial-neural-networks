import pygame as pg
import numpy as np


class Bird:

	_BIRD_COUNT = 0
	_GRAVITY = 5

	def __init__(self):

		self.bird_num = Bird._BIRD_COUNT
		Bird._BIRD_COUNT += 1
		self.bird = pg.Rect(65, 50, 50, 50)
		self.restart()


	def restart(self):

		self.birdY = 350
		self.jump = self.sprite = self.dist_wall = self.dist_middle = 0
		self.dead = self.out_of_screen = False
		self.jumpSpeed = 10
		self.gravity = Bird._GRAVITY
		self.fitness = self.final_speed = None


	def flap(self):

		if not self.dead:
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


	def update(self, upRect, downRect, middle_wall_x, middle_gap_y, travelled_dist, speed):

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
			self.fitness = travelled_dist

			if upRect.colliderect(self.bird) or downRect.colliderect(self.bird):
				self.dead = True
				self.final_speed = speed
			
			if not 0 < self.bird[1] < 720:
				self.dead = True
				self.final_speed = speed
				self.out_of_screen = True

		elif not 0 < self.bird[1] < 720:
			self.out_of_screen = True



