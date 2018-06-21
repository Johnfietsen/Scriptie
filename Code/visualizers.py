

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
	colour_nodes = {}

	for tag in simulation.generations[1].population[1].tactic:

		graph[tag] = nx.Graph()
		colour_nodes[tag] = []

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / (simulation.pop_size + dist_mutated)

	for generation in simulation.generations:

		for agent in generation.population:

			for tag in graph:

				if agent.tactic == nash:

					colour_nodes[tag].append('blue')

				elif agent.tactic[tag] == nash[tag]:

					colour_nodes[tag].append('steelblue')

				else:

					colour_nodes[tag].append('grey')

				graph[tag].add_node(agent.id)

			pos[agent.id] = [agent.gen * factor_x,
							 (agent.id - 1000 * agent.gen) * factor_y]

			if agent.type == 'normal':

				pos[agent.id][1] += dist_mutated

			if agent.type != 'mutated':

				for tag in agent.parents:

					if agent.tactic[tag] == nash[tag]:

						colour = 'steelblue'

					else:

						colour = 'grey'

					graph[tag].add_edge(agent.parents[tag], agent.id,
										colour=colour)

	return graph, pos, colour_nodes


def show_network(graph, pos, colour_nodes):

	i = 0

	for tag in graph:

		i += 1

		plt.subplot(23 * 10 + i).set_title(tag)
		edges, colours = zip(*nx.get_edge_attributes(graph[tag],'colour') \
							 .items())
		nx.draw(graph[tag], pos, node_size=10, edgelist=edges,
				node_color=colour_nodes[tag],
				arrowstyle='->', arrowsize=20, edge_color=colours,
				width=0.5)

	plt.show()


def create_path(simulation, nash):

	copy_simulation = cp.deepcopy(simulation)

	for generation in copy_simulation.generations:

		for agent in generation.population:

			print(agent.tactic)

			if agent.tactic != nash:

				print('no')

				agent.parents = {}

			else:

				print('yes')

				new_parents = {}

				for tag in agent.parents:

					if agent.parents[tag] == nash[tag]:

						new_parents[tag] = agent.parents[tag]

				agent.parents = new_parents

	return copy_simulation
