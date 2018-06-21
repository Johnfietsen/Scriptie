

import networkx as nx
import matplotlib.pyplot as plt
import copy as cp


def create_lists(simulation):

	info = {}
	sums = {}

	for tag in simulation.generations[1].population[1].tactic:

		info[tag] = []

	for generation in simulation.generations:

		for tag in info:

			sums[tag] = 0

		pop_size = len(generation.population)

		for agent in generation.population:

			if agent.type != 'mutated':

				for tag in info:

					sums[tag] += agent.tactic[tag] / pop_size

		for tag in info:

			info[tag].append(sums[tag])

	return info


def plot_results(info):

	fig = plt.figure(1)

	i = 0

	for tag in info:

		i += 1

		ax = fig.add_subplot(23 * 10 + i)
		ax.plot(info[tag], 'black')
		ax.set_title(tag)

	plt.show()


def create_network(simulation, nash):

	dist_mutated = 0.05

	graph = {}
	pos = {}

	for tag in simulation.generations[1].population[1].tactic:

		graph[tag] = nx.Graph()

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / (simulation.pop_size + dist_mutated)

	for generation in simulation.generations:

		for agent in generation.population:

			for tag in graph:

				if agent.tactic == nash:

					colour_node = 'blue'

				elif agent.tactic[tag] == nash[tag]:

					colour_node = 'steelblue'

				else:

					colour_node = 'grey'

				graph[tag].add_node(agent.id, colour=colour_node)

				if agent.type != 'mutated':

					for tag in agent.parents:

						if agent.tactic[tag] == nash[tag]:

							colour_edge = 'steelblue'

						else:

							colour_edge = 'grey'

						graph[tag].add_edge(agent.parents[tag].id, agent.id,
											colour=colour_edge)

			pos[agent.id] = [agent.gen * factor_x,
							 (agent.id - 1000 * agent.gen) * factor_y]

			if agent.type == 'normal':

				pos[agent.id][1] += dist_mutated

	return graph, pos


def show_network(graph, pos):

	i = 0

	for tag in graph:

		i += 1

		plt.subplot(23 * 10 + i).set_title(tag)
		edges, colours_edges = zip(*nx.get_edge_attributes(graph[tag],'colour')\
								   .items())
		nodes, colours_nodes = zip(*nx.get_node_attributes(graph[tag],'colour')\
								   .items())
		nx.draw(graph[tag], pos, node_size=10, edgelist=edges,
				node_color=colours_nodes, arrowstyle='->', arrowsize=20,
				edge_color=colours_edges, width=0.5)

	plt.show()


def create_path(simulation, nash):

	dist_mutated = 0.05

	graph = {}
	pos = {}

	nash_list = []

	for tag in simulation.generations[1].population[1].tactic:

		graph[tag] = nx.Graph()

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / (simulation.pop_size + dist_mutated)

	for tag in graph:

		for generation in simulation.generations:

			for agent in generation.population:

				if agent.tactic == nash:

					colour_node = 'blue'
					nash_list.append(agent)

				else:

					colour_node = 'grey'

				graph[tag].add_node(agent.id, colour=colour_node)

			pos[agent.id] = [agent.gen * factor_x,
							 (agent.id - 1000 * agent.gen) * factor_y]

			if agent.type == 'normal':

				pos[agent.id][1] += dist_mutated

		for agent in nash_list:

			graph[tag] = find_path(agent, graph, tag)

	return graph, pos


def find_path(agent, graph, tag):

	graph[tag].add_edge(agent.parents[tag].id, agent.id, colour='steelblue')

	while agent.parents[tag] != None:

		graph[tag] = find_path(agent.parents[tag], graph, tag)

	return graph[tag]
