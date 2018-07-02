

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
						path_network2, one_histogram, plot_results


# rnd.seed(5)

alpha = 0.5
pop_size = 100
nr_mutated = 2
nr_games = 50
nr_generations = 10
nr_sims = 10
bucket_size = 25

nash = {'u + r' : 1,
		'u + b' : 1,
		'r + r' : 1,
		'r + b' : 1,
		'b + r' : 1,
		'b + b' : 1}

start_time = time.time()

sims = []

bucket_1 = []
bucket_2 = []
bucket_3 = []

# for i in range(0, nr_sims):

i = 0

while len(bucket_3) < bucket_size:

	sims.append(Simulation(1, alpha, pop_size, nr_mutated, nr_games))
	sims[i].iterate(nr_generations)

	counter = 0

	# for generation in sims[i].generations:
	#
	# 	for agent in generation.population:
	#
	# 		if agent.tactic == nash:
	#
	# 			counter += 1

	for agent in sims[i].generations[nr_generations].population:

		if agent.tactic == nash:

			counter += 1

	if counter < 0.33 * pop_size: # * nr_generations:

		bucket_1.append(sims[i])

	elif counter < 0.67 * pop_size: # * nr_generations:

		bucket_2.append(sims[i])

	elif counter < 1.00 * pop_size: # * nr_generations:

		bucket_3.append(sims[i])

	i += 1

	print('0.33', len(bucket_1))
	print('0.66', len(bucket_2))
	print('1.00', len(bucket_3))

print("--- final ---")

print('0.33', len(bucket_1))
print('0.66', len(bucket_2))
print('1.00', len(bucket_3))

print("---  ---  ---")

results = centrality_measures(bucket_3, nash, 'standard')
plot_results(nr_sims, results, 'standard')

results = centrality_measures(bucket_3, nash, 'path')
plot_results(nr_sims, results, 'path')

print("--- %s seconds ---" % (time.time() - start_time))
