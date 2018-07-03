

import numpy.random as rnd
import copy as cp

from Classes.player import Player
from Classes.game import Game
from Classes.group import Group


class Generation(object):

	def __init__(self, id, pop_size, nr_mutated):

		self.id = id
		self.pop_size = pop_size
		self.nr_mutated = nr_mutated

		self.population = self.create_population()
		self.groups = None


	def create_population(self):

		population = []

		for i in range(0, self.pop_size):

			population.append(Player(self.id * 1000 + i, self.id,
									 'normal'))

		for i in range(0, self.nr_mutated):

			population[i].type = 'mutated'

		return population


	def assign_random(self):

		for agent in self.population:

			agent.random_tactic()


	def assign_by_fitness(self, fitness_list):

		for agent in self.population:

			if agent.type == 'mutated':

				agent.random_tactic()

			else:

				agent.fitness_tactic(fitness_list)


	def calc_fitness(self):

		total = 0

		for agent in self.population:

			if agent.score > 0 and agent.type != 'mutated':

				total += agent.score

		total += total * (self.nr_mutated / self.pop_size)

		for agent in self.population:

			if agent.type == 'mutated':

				agent.fitness = self.nr_mutated / self.pop_size

			elif agent.score > 0:

				agent.fitness = agent.score / total

			else:

				agent.fitness = 0


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

			for i in range(0, int(self.pop_size / 2)):

				while any(elem in j for elem in list_1) or j == [None]:

					j[0] = rnd.randint(0, self.pop_size)

				list_1.append(j[0])

			for i in range(0, int(self.pop_size / 2)):

				while any(elem in j for elem in list_2) or \
					  any(elem in j for elem in list_1):

					j[0] = rnd.randint(0, self.pop_size)

				list_2.append(j[0])

			for i in range(0, int(self.pop_size / 2)):

				game = Game(self.population[list_1[i]],
							self.population[list_2[i]], alpha)

				game.play()


	def create_groups(self):

		self.groups = {}

		tactic_format = {}

		i = 1

		for tag in self.population[0].tactic:

			i *= 2
			tactic_format[tag] = None

		for j in range(0, i):

			b_tactic = format(j, "06b")

			k = 0

			tactic = cp.deepcopy(tactic_format)

			for tag in tactic:

				tactic[tag] = int(b_tactic[k])

				k += 1

			self.groups[b_tactic] = Group(self.id * 1000 + j, self.id, tactic,
										  self, b_tactic)

		for tag_2 in self.groups:

			self.groups[tag_2].find_parents(self)
