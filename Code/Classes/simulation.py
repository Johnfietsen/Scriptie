

import numpy.random as rnd

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game


class Simulation(object):

	def __init__(self, id, alpha, pop_size, nr_games):

		self.id = id
		self.alpha = alpha
		self.pop_size = pop_size
		self.nr_games = nr_games

		self.generations = self.create_first()


	def create_first(self):

		first = Generation(0, self.pop_size)
		first.assign_random()

		return [first]


	def iterate(self, nr_iterations):

		for i in range(1, nr_iterations + 1):

			print('generation', i)

			previous = self.generations[i - 1]

			previous.play_games(self.nr_games, self.alpha)

			next = Generation(i, self.pop_size)
			next.assign_by_fitness(previous.create_fitness_list())

			self.generations.append(next)
