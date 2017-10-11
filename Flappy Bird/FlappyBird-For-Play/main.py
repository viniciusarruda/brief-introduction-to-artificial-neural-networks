#!/usr/bin/env python

from flappybird import FlappyBird
from bird import Bird

def main():

	best = None
	best_speed = None
	tmp_speed = None

	fp = FlappyBird()
	bird = Bird()
	best_speed = fp.run(bird, best, best_speed)
	best = bird

	while True:
		
		bird = Bird()
		tmp_speed = fp.run(bird, best, best_speed)

		if bird.fitness > best.fitness:
			best = bird
			best_speed = tmp_speed


if __name__ == "__main__":
	main()

