import numpy as np
from random import randint, random, uniform, shuffle

class GeneticAlgorithm:

	def __init__(self, _n_individuals, _new_individual):

		self.best_fitness = self.best_id = self.best_brain = None
		self.mutation_rate = 0.4
		self.parents_rate = 0.4
		self.copy_rate = 0.2   # has to be lower than parents_rate
		self.crossover_rate = 0.4
		self.n_individuals = _n_individuals
		self.new_individual = _new_individual


	def init_population(self):

		return [self.new_individual(None) for _ in xrange(self.n_individuals)]


	def _mutate(self, individual):

		for l, c in np.ndindex(individual.shape):
			if random() < self.mutation_rate:
				individual[l, c] += uniform(-0.1, 0.1)


	def _crossover(self, male, female):   

		c = male.shape[1] / 2
		return np.concatenate((male[:, :c], female[:, c:]), axis=1)


	def evolve(self, population):

		population = list(zip(*sorted(zip(map(lambda individual: individual.fitness, population), population), key=lambda t: t[0]))[1])

		best = (population[-1].bird_num, population[-1].final_speed, population[-1].fitness, np.copy(population[-1].brain))

		n_parents = int(self.parents_rate * self.n_individuals)
		parents = population[-n_parents:]
		n_children = int(self.crossover_rate * self.n_individuals)

		parents_brain = map(lambda individual: individual.brain, parents)

		children = []
		children.append(self._crossover(parents_brain[-2], parents_brain[-1]))

		while len(children) < n_children:
			male, female = randint(0, n_parents-1), randint(0, n_parents-1)
			if male != female:
				children.append(self._crossover(parents_brain[male], parents_brain[female]))

		n_copies = int(self.copy_rate * self.n_individuals)
		index = range(len(parents_brain))
		shuffle(index)
		index = index[:n_copies]

		for i in index:
			children.append(np.copy(parents_brain[i]))

		for individual in children:
			self._mutate(individual)

		for individual in parents:
			individual.restart()

		population = parents

		for individual in children:
			population.append(self.new_individual(individual))

		return population, best

