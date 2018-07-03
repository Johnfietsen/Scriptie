

import numpy.random as rnd
import matplotlib.pyplot as plt
import time

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game
from Classes.simulation import Simulation
from visualizers import create_lists, plot_results, standard_network, \
						six_networks, path_network, phenotype_network, \
						show_network, six_histograms, centrality_measures, \
						path_network2, one_histogram, plot_results, \
						standard_network2


rnd.seed(4)

alpha = 0.5
pop_size = 100
nr_mutated = int(0.06 * pop_size)
pop_size +=  nr_mutated
nr_games = 50
nr_generations = 10
nr_sims = 25
bucket_size = 25

nash = {'u + r' : 1,
		'u + b' : 1,
		'r + r' : 1,
		'r + b' : 1,
		'b + r' : 1,
		'b + b' : 1}


start_time = time.time()

sims = []

for i in range(0, nr_sims):

	sims.append(Simulation(i, alpha, pop_size, nr_mutated, nr_games))
	sims[i].iterate(nr_generations)

	counter = 0

	for agent in sims[i].generations[nr_generations].population:

		if agent.tactic == nash:

			counter += 1

	for agent in sims[i].generations[0].population:

		if agent.tactic == nash:

			counter -= 1

results = centrality_measures(sims, nash, 'standard')
plot_results(nr_sims, results, 'standard')

results = centrality_measures(sims, nash, 'path')
plot_results(nr_sims, results, 'path')

print("--- %s seconds ---" % (time.time() - start_time))
