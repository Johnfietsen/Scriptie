

import numpy as np
import numpy.random as rnd

from Classes.player import Player
from Classes.game import Game


class Generation(object):

	def __init__(self, id, pop_size):

		self.id = id
		self.population = self.create_population(pop_size)


	def create_population(self, pop_size):

		population = []

		for i in range(0, pop_size):

			population.append(Player(i))

		return population


	def assign_random(self):

		for agent in self.population:

			agent.random_tactic()


	def assign_by_fitness(self, fitness_list):

		for agent in self.population:

			agent.fitness_tactic(fitness_list)


	def calc_fitness(self):

		total = 0

		for agent in self.population:

			if agent.score > 0:

				total += agent.score

		for agent in self.population:

			if agent.score <= 0:

				agent.fitness = 0

			else:

				agent.fitness = agent.score / total


	def create_fitness_list(self):

		self.calc_fitness()

		list = []

		for agent in self.population:

			for i in range(0, int(agent.fitness * 200)):

				list.append(agent)

		return list


	def play_games(self, nr_rounds, alpha):

		for i in range(0, nr_rounds):

			list_1 = []
			list_2 = []

			j = [None]

			for i in range(0, int(len(self.population) / 2)):

				while any(elem in j for elem in list_1) or j == [None]:

					j[0] = rnd.randint(0, len(self.population))

				list_1.append(j[0])

			for i in range(0, int(len(self.population) / 2)):

				while any(elem in j for elem in list_2) or \
					  any(elem in j for elem in list_1):

					j[0] = rnd.randint(0, len(self.population))

				list_2.append(j[0])

			for i in range(0, int(len(self.population) / 2)):

				game = Game(self.population[list_1[i]],
							self.population[list_2[i]], alpha)

				game.play()
