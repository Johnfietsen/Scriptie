

import numpy.random as rnd

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game


# rnd.seed(4)

test = Generation(1, 100)
test.assign_random()
test.play_games(200, 0.4)

total_points = 0

for agent in test.population:

	# print(agent.score)

	if agent.score > 0:

		total_points += agent.score

# print(total_points)

# hoi = 0

for agent in test.population:

	if agent.score > 0:

		agent.fitness = int(agent.score / total_points * 1000)

	else:

		agent.fitness = 0

	# hoi += agent.fitness

# print(hoi)

fitness_list = []

for agent in test.population:

	for i in range(0, agent.fitness):

		fitness_list.append(agent)

# print(fitness_list)

test2 = Generation(2, 100)
test2.assign_by_fitness(fitness_list)
test2.play_games(200, 0.4)
