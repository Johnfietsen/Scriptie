

import networkx as nx
import matplotlib.pyplot as plt
import copy as cp

sns = 5

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


def standard_network2(simulation, nash):

	dist_mutated = 0.05

	graph = nx.DiGraph()
	pos = {}

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / (simulation.pop_size + dist_mutated)

	for tag in simulation.generations[1].population[1].tactic:

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

				graph.add_node(agent.id, colour=colour_node)

				if agent.parents != {}:

					if agent.tactic[tag] == nash[tag]:

						colour_edge = 'steelblue'

					else:

						colour_edge = 'grey'

					graph.add_edge(agent.parents[tag].id, agent.id,
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
		nx.draw(graph[tag], pos, node_size=sns, edgelist=edges,
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

						graph = find_path2(agent, graph, nash,
										   simulation.pop_size)

		# for generation in simulation.generations:
		#
		# 	for agent in generation.population:
		#
		# 		if not graph.has_node(agent.id):
		#
		# 			graph.add_node(agent.id, colour='grey')

	return graph, pos


def find_path2(agent, graph, nash, pop_size):

	for tag in agent.parents:

		if agent.parents[tag].tactic[tag] == nash[tag]:

			if not graph.has_node(agent.parents[tag].id):

				graph.add_node(agent.parents[tag].id, colour='steelblue')

			if not graph.has_edge(agent.parents[tag].id, agent.id):

				graph.add_edge(agent.parents[tag].id, agent.id,
							   colour='steelblue',
							   weight=1 / pop_size)

				if agent.parents[tag].parents != {}:

					graph = find_path2(agent.parents[tag], graph, nash,
									   pop_size)

			else:

				graph[agent.parents[tag].id][agent.id]['weight'] += 1 / pop_size

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

		nx.draw(graph, pos, node_size=sns, edgelist=edges,
				node_color=colours_nodes, arrowstyle='->', arrowsize=1,
				edge_color=colours_edges, width = 0.2)

	elif sizes == 'weights':

		weights = [graph[u][v]['weight'] for u,v in edges]

		nx.draw(graph, pos, node_size=sns, edgelist=edges,
				node_color=colours_nodes, arrowstyle='->', arrowsize=1,
				edge_color=colours_edges, width=weights)

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

			graph, pos = standard_network(simulations[i], nash)

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


def one_histogram(simulations, nash, type):

	list_outdegree = []

	for i in range(0, len(simulations)):

		if type == 'standard':

			graph, pos = standard_network(simulations[i], nash)

		elif type == 'path':

			graph, pos = path_network2(simulations[i], nash)

		elif type == 'pheno':

			graph, pos, sizes = phenotype_network(simulations[i])

		nodes_list = {}
		outdegree = {}

		nodes_list = list(graph.nodes)

		outdegree = graph.out_degree(nodes_list, weight='weight' * \
									 simulations[0].pop_size)

		tmp_list = []

		for pair in outdegree:

			tmp_list.append(pair[1])

		list_outdegree.append(tmp_list)

	plt.hist(list_outdegree, bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
			 alpha=0.5)

	plt.show()


def plot_results(nr_sims, results, type):

	list_hist = {}

	for tag in results:

		if tag != 'connectivity' and tag != 'density':

			list_hist[tag] = []

			for sim in results[tag]:

				tmp_list = []

				for pair in sim:

					tmp_list.append(sim[pair])

				list_hist[tag].append(tmp_list)

			plt.hist(list_hist[tag], #bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
					 alpha=1)

			plt.savefig('Results/' + type + ' ' + tag + '.png',
						bbox_inches='tight')

			plt.clf()



	# j = 0
	#
	# for tag in results:
	#
	# 	if tag != 'connectivity' and tag != 'density':
	#
	# 		j += 1
	#
	# 		plt.subplot(23 * 10 + j).set_title(tag)
	#
	# 		plt.hist(list_hist[tag], #bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	# 				 alpha=0.5, label=str(j))
	#
	# plt.show()


def centrality_measures(simulations, nash, type):

	results = {'closeness' : [],
			   'betweenness' : [],
			   'katz' : [],
			   'degree' : [],
			   'load' : [],
			   'connectivity' : [],
			   'density' : []}

	i = 0

	for simulation in simulations:

		i += 1

		if type == 'standard':

			graph, pos = standard_network2(simulation, nash)

			print('standard', i)

		elif type == 'path':

			graph, pos = path_network2(simulation, nash)

			print('path', i)


		elif type == 'pheno':

			graph, pos, sizes = phenotype_network(simulation)

			print('pheno', i)

		results['closeness'].append(nx.closeness_centrality(graph,
															distance='weight'))
		results['betweenness'].append(nx.betweenness_centrality(graph,
															weight='weight'))
		results['katz'].append(nx.katz_centrality(graph, weight='weigth'))
		results['degree'].append(nx.degree_centrality(graph))
		results['load'].append(nx.load_centrality(graph, weight='weight'))

		# results['connectivity'].append(nx.node_connectivity(graph))
		# results['density'].append(nx.density(graph))

	return results
