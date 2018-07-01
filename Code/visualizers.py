

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


def standard_network(simulation, nash):

	dist_mutated = 0.05

	graph = {}
	pos = {}

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / (simulation.pop_size + dist_mutated)

	for tag in simulation.generations[1].population[1].tactic:

		graph[tag] = nx.DiGraph()

		for generation in simulation.generations:

			for agent in generation.population:

				pos[agent.id] = [agent.gen * factor_x,
								 (agent.id - 1000 * agent.gen) * factor_y]

				if agent.type == 'normal':

					pos[agent.id][1] += dist_mutated

				if agent.tactic == nash:

					colour_node = 'blue'

				elif agent.tactic[tag] == nash[tag]:

					colour_node = 'steelblue'

				else:

					colour_node = 'grey'

				graph[tag].add_node(agent.id, colour=colour_node)

				if agent.parents != {}:

					if agent.tactic[tag] == nash[tag]:

						colour_edge = 'steelblue'

					else:

						colour_edge = 'grey'

					graph[tag].add_edge(agent.parents[tag].id, agent.id,
										colour=colour_edge)

	return graph, pos


def six_networks(graph, pos):

	i = 0

	for tag in graph:

		i += 1

		plt.subplot(23 * 10 + i).set_title(tag)
		edges, colours_edges = zip(*nx.get_edge_attributes(graph[tag],'colour')\
								   .items())
		nodes, colours_nodes = zip(*nx.get_node_attributes(graph[tag],'colour')\
								   .items())
		nx.draw(graph[tag], pos, node_size=10, edgelist=edges,
				node_color=colours_nodes, arrowstyle='->', arrowsize=1,
				edge_color=colours_edges, width=0.5)

	plt.show()


def path_network(simulation, nash):

	dist_mutated = 0.05

	graph = {}
	pos = {}

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / (simulation.pop_size + dist_mutated)

	for tag in simulation.generations[0].population[0].tactic:

		graph[tag] = nx.DiGraph()

		for generation in simulation.generations:

			for agent in generation.population:

				pos[agent.id] = [agent.gen * factor_x,
								 (agent.id - 1000 * agent.gen) * factor_y]

				if agent.type == 'normal':

					pos[agent.id][1] += dist_mutated

				if agent.tactic == nash:

					graph[tag].add_node(agent.id, colour='blue')

					if agent.type == 'normal' and generation.id != 0:

						graph = find_path(agent, graph, tag)

		# for generation in simulation.generations:
		#
		# 	for agent in generation.population:
		#
		# 		if not graph[tag].has_node(agent.id):
		#
		# 			graph[tag].add_node(agent.id, colour='grey')

	return graph, pos


def find_path(agent, graph, tag):

	if not graph[tag].has_node(agent.parents[tag].id):

		graph[tag].add_node(agent.parents[tag].id, colour='steelblue')

	graph[tag].add_edge(agent.parents[tag].id, agent.id, colour='steelblue')

	if agent.parents[tag].parents != {}:

		graph = find_path(agent.parents[tag], graph, tag)

	return graph


def path_network2(simulation, nash):

	dist_mutated = 0.05

	graph = nx.DiGraph()
	pos = {}

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / (simulation.pop_size + dist_mutated)

	for tag in simulation.generations[0].population[0].tactic:

		for generation in simulation.generations:

			for agent in generation.population:

				pos[agent.id] = [agent.gen * factor_x,
								 (agent.id - 1000 * agent.gen) * factor_y]

				if agent.type == 'normal':

					pos[agent.id][1] += dist_mutated

				if agent.tactic == nash:

					graph.add_node(agent.id, colour='blue')

					if agent.type == 'normal' and generation.id != 0:

						graph = find_path2(agent, graph, nash)

		# for generation in simulation.generations:
		#
		# 	for agent in generation.population:
		#
		# 		if not graph[tag].has_node(agent.id):
		#
		# 			graph[tag].add_node(agent.id, colour='grey')

	return graph, pos


def find_path2(agent, graph, nash):

	for tag in agent.parents:

		if agent.parents[tag].tactic[tag] == nash[tag]:

			if not graph.has_node(agent.parents[tag].id):

				graph.add_node(agent.parents[tag].id, colour='steelblue')

			graph.add_edge(agent.parents[tag].id, agent.id, colour='steelblue')

			if agent.parents[tag].parents != {}:

				graph = find_path2(agent.parents[tag], graph, nash)

	return graph


def phenotype_network(simulation):

	graph = nx.DiGraph()
	pos = {}
	sizes = []

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / len(simulation.generations[1].groups)

	for i in range(1, len(simulation.generations)):

		for tag in simulation.generations[i].groups:

			group = simulation.generations[i].groups[tag]

			pos[group.id] = [group.gen * factor_x,
							 (group.id - 1000 * group.gen) * factor_y]

			sizes.append(len(group.population))

			graph.add_node(group.id, colour='blue')

		if i > 1:

			for tag in simulation.generations[i].groups:

				group = simulation.generations[i].groups[tag]

				for tag_2 in group.parents:

					weight = (group.parents[tag_2] / simulation.pop_size)

					graph.add_edge(simulation.generations[i - 1].groups[tag_2]\
								   .id, group.id, colour='black', weight=weight)

	return graph, pos, sizes


def show_network(graph, pos, sizes=None):

	edges, colours_edges = zip(*nx.get_edge_attributes(graph,'colour')\
							   .items())

	nodes, colours_nodes = zip(*nx.get_node_attributes(graph,'colour')\
							   .items())

	if sizes == None:

		nx.draw(graph, pos, node_size=10, edgelist=edges,
				node_color=colours_nodes, arrowstyle='->', arrowsize=1,
				edge_color=colours_edges, width = 0.2)

	else:

		weights = [graph[u][v]['weight'] for u,v in edges]

		nx.draw(graph, pos, node_size=sizes, edgelist=edges,
				node_color=colours_nodes, arrowstyle='->', arrowsize=1,
				edge_color=colours_edges, width=weights)

	plt.show()


def six_histograms(simulations, nash, type):

	list_outdegree = {}

	for tag in simulations[0].generations[0].population[0].tactic:

		list_outdegree[tag] = []

	for i in range(0, len(simulations)):

		if type == 'path':

			graph, pos = path_network(simulations[i], nash)

		elif type == 'all':

			graph, pos = standard_network(simulations[i],  nash)

		nodes_list = {}
		outdegree = {}

		for tag in graph:

			nodes_list[tag] = list(graph[tag].nodes)

			outdegree[tag] = graph[tag].out_degree(nodes_list[tag])

			tmp_list = []

			for pair in outdegree[tag]:

				tmp_list.append(pair[1])

			list_outdegree[tag].append(tmp_list)

			if tmp_list == []:

				print('empty', tag, i)

	j = 0

	for tag in list_outdegree:

		j += 1

		plt.subplot(23 * 10 + j).set_title(tag)

		plt.hist(list_outdegree[tag], bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
				 alpha=0.5, label=str(j))

	plt.show()


def centrality_measures(simulations, nash):

	results = {'closeness' : [],
			   'betweenness' : [],
			   'katz' : [],
			   'degree' : [],
			   'load' : [],
			   'connectivity' : [],
			   'density' : []}

	for i in range(0, len(simulations)):

		graph, pos = path_network(simulations[i], nash)

		results['closeness'].append(nx.closeness_centrality(graph['u + r']))
		results['betweenness'].append(nx.betweenness_centrality(graph['u + r']))
		results['katz'].append(nx.katz_centrality(graph['u + r']))
		results['degree'].append(nx.degree_centrality(graph['u + r']))
		results['load'].append(nx.load_centrality(graph['u + r']))
		results['connectivity'].append(nx.node_connectivity(graph['u + r']))
		results['density'].append(nx.density(graph['u + r']))

	return results
