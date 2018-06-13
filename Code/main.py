

import numpy.random as rnd
import copy

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game


rnd.seed(6)


def next_generation(nr_generations, previous, nr_games, alpha):

	for i in range(0, nr_generations):

		previous.play_games(nr_games, alpha)

		total_points = 0

		for agent in previous.population:

			if agent.score > 0:

				total_points += agent.score

		for agent in previous.population:

			if agent.score > 0:

				agent.fitness = int(agent.score / total_points * 1000)

			else:

				agent.fitness = 0

		fitness_list = []

		for agent in previous.population:

			print('player ', agent.id, '   fitness ', agent.fitness)

			for j in range(0, agent.fitness):

				fitness_list.append(copy.deepcopy(agent))

		# print(len(fitness_list))

		next = Generation(previous.id + 1, len(previous.population))
		next.assign_by_fitness(fitness_list)
		next.play_games(nr_games, alpha)

		print('generation ', i)

		previous = next

	return next

first = Generation(1, 100)
first.assign_random()

last = next_generation(1000, first, 20, 0.4)
