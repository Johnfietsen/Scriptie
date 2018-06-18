

import numpy.random as rnd

from Classes.player import Player
from Classes.generation import Generation
from Classes.game import Game
from Classes.simulation import Simulation
from visualizers import create_lists, plot_results


# rnd.seed(6)

alpha = 0.4
pop_size = 100
nr_games = 100

test = Simulation(1, alpha, pop_size, nr_games)
test.iterate(50)

plot_results(create_lists(test))
