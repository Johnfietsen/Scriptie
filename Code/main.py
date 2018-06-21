

import numpy.random as rnd

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game
from Classes.simulation import Simulation
from visualizers import create_lists, plot_results, create_network, \
						show_network, create_path


# rnd.seed(6)

alpha = 0.4
pop_size = 10
nr_mutated = 0
nr_games = 100
nr_generations = 10

nash = {'u + r' : 1,
		'u + b' : 1,
		'r + r' : 1,
		'r + b' : 1,
		'b + r' : 1,
		'b + b' : 1}

test = Simulation(1, alpha, pop_size, nr_mutated, nr_games)
test.iterate(nr_generations)

# graph, pos = create_network(test, nash)
# show_network(graph, pos)

graph, pos = create_path(test, nash)
show_network(graph, pos)

# plot_results(create_lists(test))
