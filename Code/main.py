

import numpy.random as rnd

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game
from Classes.simulation import Simulation
from visualizers import create_lists, plot_results


# rnd.seed(6)

alpha = 0.1
pop_size = 10
nr_games = 100

for i in range(0, 1):

	test = Simulation(1, alpha, pop_size, nr_games)
	test.iterate(100)

	plot_results(create_lists(test))
