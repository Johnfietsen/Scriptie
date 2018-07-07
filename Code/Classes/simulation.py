

import numpy.random as rnd

from Classes.generation import Generation


class Simulation(object):

	def __init__(self, id, alpha, pop_size, nr_mutated, nr_games):

		self.id = id
		self.alpha = alpha
		self.pop_size = pop_size
		self.nr_mutated = nr_mutated
		self.nr_games = nr_games

		self.generations = self.create_first()


	def create_first(self):

		first = Generation(0, self.pop_size, self.nr_mutated)
		first.assign_random()

		return [first]


	def iterate(self, nr_iterations):

		for i in range(1, nr_iterations + 1):

			# print('generation', i)

			previous = self.generations[i - 1]

			previous.play_games(self.nr_games, self.alpha)

			next = Generation(i, self.pop_size, self.nr_mutated)
			next.assign_by_fitness(previous.create_fitness_list())
			next.create_groups()

			self.generations.append(next)
