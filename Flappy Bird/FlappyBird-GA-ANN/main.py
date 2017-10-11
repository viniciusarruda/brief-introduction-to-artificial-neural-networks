#!/usr/bin/env python

from flappybird import FlappyBird
from genetic_algorithm import GeneticAlgorithm
from bird import Bird


def show_best(best_info):

	print ('Best bird:    \n' +
	       'ID:         {}\n' +
	       'Generation: {}\n' +
	       'Fitness:    {}\n' +
	       'Brain:\n{}\n'
	      ).format(best_info[0], best_info[4], best_info[2], best_info[3])


def main():

	n_birds = 15
	n_generations = 1000
	best_info = None

	fp = FlappyBird()
	ga = GeneticAlgorithm(n_birds, lambda brain: Bird(_brain=brain))
	birds = ga.init_population() 

	fp.run(birds, best_info)
	birds, best_info = ga.evolve(birds)
	best_info = best_info + (1, )
	show_best(best_info)

	for i in xrange(n_generations):
		fp.run(birds, best_info)
		birds, tmp = ga.evolve(birds)

		if tmp[2] > best_info[2]:
			best_info = tmp + (i + 2, )
			show_best(best_info)


if __name__ == "__main__":
	main()

