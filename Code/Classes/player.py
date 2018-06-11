

import numpy as np
import numpy.random as rnd


class Player(object):

	def __init__(self, id):

		self.id = id
		self.tactic_1 = self.empty_tactic()
		self.tactic_2 = self.empty_tactic()
		self.score = 0
		self.fitness = 0
		self.card = None


	def decide_move(self, game, player_nr):

		alpha = str(game.alpha)
		stakes = str(game.stakes)

		if player_nr == 1:

			return \
			   self.tactic_1[alpha][self.card][game.main_card][stakes]

		elif player_nr == 2:

			return \
			   self.tactic_2[alpha][self.card][game.main_card][stakes]

		else:

			print('invalid player number')

			return


	def empty_tactic(self):

		tactic = {'0.2' : None, '0.4' : None, '0.6' : None, '0.8' : None}

		for alpha in tactic:

			tactic[alpha] = {'red' : None, 'black' : None}

			for card in tactic[alpha]:

					tactic[alpha][card] = {'red' : None, 'black' : None,
										   'unknown' : None}

					for card_m in tactic[alpha][card]:

						tactic[alpha][card][card_m] = {'0' : None, '1' : None,
													   '2' : None, '3' : None,
													   '4' : None, '5' : None,
													   '6' : None}

						for stake in tactic[alpha][card][card_m]:

							tactic[alpha][card][card_m][stake] = None

		return tactic


	def random_tactic(self, player_nr):

		if player_nr == 1:

			tactic = self.tactic_1

		elif player_nr == 2:

			tactic = self.tactic_2

		for alpha in tactic:

			for card in tactic[alpha]:

					for card_m in tactic[alpha][card]:

						for stake in tactic[alpha][card][card_m]:

							if player_nr == 1:

								i = rnd.randint(0, 3)

								if i == 0:

									move = 'fold'

								elif i == 1:

									move = 'check'

								elif i == 2:

									move = 'raise'

								tactic[alpha][card][card_m][stake] = move

							elif player_nr == 2:

									i = rnd.randint(0, 2)

									if i == 0:

										move = 'fold'

									elif i == 1:

										move = 'check'

									tactic[alpha][card][card_m][stake] = move

		return tactic


	def fitness_tactic(self, player_nr, fitness_list):

		if player_nr == 1:

			tactic = self.tactic_1

		elif player_nr == 2:

			tactic = self.tactic_2

		for alpha in tactic:

			for card in tactic[alpha]:

					for card_m in tactic[alpha][card]:

						for stake in tactic[alpha][card][card_m]:

							i = rnd.randint(0, len(fitness_list))

							if player_nr == 1:

								move = fitness_list[i]\
										.tactic_1[alpha][card][card_m][stake]

							elif player_nr == 2:

								move = fitness_list[i]\
										.tactic_2[alpha][card][card_m][stake]

							tactic[alpha][card][card_m][stake] = move

		return tactic
