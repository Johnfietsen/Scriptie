

import numpy.random as rnd


class Game(object):

	def __init__(self, player_1, player_2, alpha):

		self.players = [player_1, player_2]
		self.alpha = alpha

		self.stakes = None
		self.main_card = 'u'


	def get_card(self):

		i = rnd.randint(1, 101)

		if i < (self.alpha * 100):

			return 'r'

		elif i >= (self.alpha * 100):

			return 'b'


	def payout(self, winner):

		if winner == 'draw':

			self.players[0].score += self.stakes / 2
			self.players[1].score += self.stakes / 2

		else:

			self.players[winner - 1].score += self.stakes

		self.stakes = None


	def round(self, round_nr):

		player_1 = self.players[0]
		player_2 = self.players[1]

		if round_nr == 1:

			player_1.score -= 1
			player_2.score -= 1
			self.stakes += 2

		move_1 = player_1.decide_move(self)

		if move_1 == 0:

			self.payout(2)

			return '1 folds'

		elif move_1 == 1:

			player_1.score -= 1
			self.stakes += 1

			move_2 = player_2.decide_move(self)

			if move_2 == 0:

				self.payout(1)

				return '2 folds'

			elif move_2 == 1:

				player_2.score -= 1
				self.stakes += 1

				return 'next round'


	def play(self):

		player_1 = self.players[0]
		player_2 = self.players[1]

		self.stakes = 0
		player_1.card = self.get_card()
		player_2.card = self.get_card()

		round = self.round(1)

		if round != 'next round':

			return round

		self.main_card = self.get_card()

		round = self.round(2)

		if round != 'next round':

			return round

		if self.main_card == player_1.card and self.main_card != player_2.card:

			self.payout(1)

			return '1 wins'

		elif self.main_card != player_1.card and \
			 self.main_card == player_2.card:

			self.payout(2)

			return '2 wins'

		else:

			self.payout('draw')

			return 'draw'
