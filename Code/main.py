

import numpy.random as rnd
import matplotlib.pyplot as plt
import copy as cp
import time

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game
from Classes.simulation import Simulation
from visualizers import show_network, centrality_measures, \
						path_network2, plot_results, save_results2, \
						standard_network2, save_results, values_network


rnd.seed(4)

alpha = 0.5
pop_size = 50
nr_mutated = int(0.06 * pop_size)
pop_size +=  nr_mutated
nr_games = 50
nr_generations = 6
nr_sims = 25

nash = {'u + r' : 1,
		'u + b' : 1,
		'r + r' : 1,
		'r + b' : 1,
		'b + r' : 1,
		'b + b' : 1}


start_time = time.time()

sims = []

for i in range(0, nr_sims):

	print('simulation', i + 1)

	sims.append(Simulation(i, alpha, pop_size, nr_mutated, nr_games))
	sims[i].iterate(nr_generations)

	counter = 0

	for agent in sims[i].generations[nr_generations].population:

		if agent.tactic == nash:

			counter += 1

	for agent in sims[i].generations[0].population:

		if agent.tactic == nash:

			counter -= 1

example = cp.deepcopy(sims[0])

# graph, pos = standard_network2(sims[0], nash)
# show_network(graph, pos, 'weights')
# graph, pos = path_network2(sims[0], nash)
# show_network(graph, pos, 'weights')

results = centrality_measures(sims, nash, 'standard')
save_results2(results, example, 'standard')
# plot_results(nr_sims, results, 'standard')
# values_network(example, results, 'standard', nash)

results = centrality_measures(sims, nash, 'path')
save_results2(results, example, 'path')
# plot_results(nr_sims, results, 'path')
# values_network(example, results, 'path', nash)

print("--- %s seconds ---" % (time.time() - start_time))
