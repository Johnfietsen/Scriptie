

import numpy.random as rnd


class Player(object):

	def __init__(self, id, generation, type):

		self.id = id
		self.gen = generation
		self.type = type

		self.tactic = self.empty_tactic()
		self.card = None

		self.score = 0
		self.fitness = None

		self.parents = {}


	def decide_move(self, game):

		return self.tactic[game.main_card + ' + ' + self.card]


	def empty_tactic(self):

		return {'u + r' : None,
				'u + b' : None,
				'r + r' : None,
				'r + b' : None,
				'b + r' : None,
				'b + b' : None}


	def random_tactic(self):

		for tag in self.tactic:

			self.tactic[tag] = rnd.randint(0, 2)


	def fitness_tactic(self, fitness_list):

		for tag in self.tactic:

			i = rnd.randint(0, len(fitness_list))

			self.tactic[tag] = fitness_list[i].tactic[tag]

			self.parents[tag] = fitness_list[i]
