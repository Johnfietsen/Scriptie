

import numpy as np
import numpy.random as rnd


class Player(object):

	def __init__(self, id):

		self.id = id
		self.tactic = self.empty_tactic()

		self.score = 0
		self.fitness = None
		self.card = None


	def decide_move(self, game):

		return self.tactic[game.main_card][self.card]


	def empty_tactic(self):

		return {'unknown' : {'red' : None, 'black' : None},
			    'red' : 	{'red' : None, 'black' : None},
		  		'black' : 	{'red' : None, 'black' : None}}


	def random_tactic(self):

		for main in self.tactic:

			for own in self.tactic[main]:

				self.tactic[main][own] = rnd.randint(0, 2)



	def fitness_tactic(self, fitness_list):

		for main in self.tactic:

			for own in self.tactic[main]:

				i = rnd.randint(0, len(fitness_list))

				self.tactic[main][own] = fitness_list[i].tactic[main][own]
