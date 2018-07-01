

import numpy.random as rnd
import matplotlib.pyplot as plt

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game
from Classes.simulation import Simulation
from visualizers import create_lists, plot_results, standard_network, \
						six_networks, path_network, phenotype_network, \
						show_network, six_histograms, centrality_measures, \
						path_network2


# rnd.seed(5)

alpha = 0.5
pop_size = 50
nr_mutated = int(0.05 * pop_size)
nr_games = 50
nr_generations = 10

nash = {'u + r' : 1,
		'u + b' : 1,
		'r + r' : 1,
		'r + b' : 1,
		'b + r' : 1,
		'b + b' : 1}

# sims = []
#
# for i in range(0, 10):
#
# 	sims.append(Simulation(1, alpha, pop_size, nr_mutated, nr_games))
# 	sims[i].iterate(nr_generations)
#
# six_histograms(sims, nash, 'path')
# results = centrality_measures(sims, nash)
#
# for tag in results:
#
# 	print(tag, results[tag])


test = Simulation(1, alpha, pop_size, nr_mutated, nr_games)
test.iterate(nr_generations)

graph, pos = path_network2(test, nash)
show_network(graph, pos)

# graph, pos, sizes = phenotype_network(test)
# show_network(graph, pos, sizes)

# graph, pos = standard_network(test, nash)
# # show_network(graph['u + r'], pos)
# six_networks(graph, pos)
#
# graph, pos = path_network(test, nash)
# # show_network(graph['u + r'], pos)
# six_networks(graph, pos)
#
# plot_results(create_lists(test))
