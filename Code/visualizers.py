

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import copy as cp
import numpy as np

sns = 5
ses = 10
params = {"figure.facecolor": "#cad9e1",
              "axes.facecolor": "white",
              "axes.grid" : True,
              "axes.grid.axis" : "y",
              "grid.color"    : "black",
              "grid.linewidth": 0.2,
              "axes.spines.left" : False,
              "axes.spines.right" : False,
              "axes.spines.top" : False,
              "ytick.major.size": 0,
              "ytick.minor.size": 0,
              "xtick.direction" : "in",
              "xtick.major.size" : 7,
              "xtick.color"      : "#191919",
              "axes.edgecolor"    :"#191919",
              "axes.prop_cycle" : plt.cycler('color',
                                    ['#006767', '#ff7f0e', '#2ca02c', '#d62728',
                                     '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                                     '#bcbd22', '#17becf'])}


def standard_network2(simulation, nash):

	poi = 0

	dist_mutated = 0.05
	pop_size = simulation.pop_size - simulation.nr_mutated

	graph = nx.DiGraph()
	pos = {}

	factor_x = 1 / len(simulation.generations)
	factor_y = 1 / (simulation.pop_size + dist_mutated)

	for tag in simulation.generations[1].population[1].tactic:

		for generation in simulation.generations:

			for agent in generation.population:

				if agent.type != 'mutated':

					pos[agent.id] = [agent.gen * factor_x,
									 (agent.id - 1000 * agent.gen) * factor_y]

					# if agent.type == 'normal':
					#
					# 	pos[agent.id][1] += dist_mutated

					if agent.tactic == nash:

						colour_node = 'blue'

					elif agent.tactic[tag] == nash[tag]:

						colour_node = 'steelblue'

					else:

						colour_node = 'grey'

					graph.add_node(agent.id, colour=colour_node)

				if agent.parents != {} and agent.parents[tag].type != 'mutated':

					if agent.tactic[tag] == nash[tag]:

						colour_edge = 'steelblue'

					else:

						colour_edge = 'grey'

					if not graph.has_edge(agent.parents[tag].id, agent.id):

						graph.add_edge(agent.parents[tag].id, agent.id,
									   colour=colour_edge,
									   weight=ses / pop_size)

					else:

						graph[agent.parents[tag].id][agent.id]['weight'] += \
																ses / pop_size
						poi +=1

	# print(poi)
	return graph, pos


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

				# if agent.type == 'normal':
				#
				# 	pos[agent.id][1] += dist_mutated

		generation = simulation.generations[len(simulation.generations) - 1]

		for agent in generation.population:

			if agent.tactic == nash and agent.type != 'mutated':

				graph.add_node(agent.id, colour='blue')

				# if agent.type == 'normal' and generation.id != 0:
				if generation.id != 0:

					graph = find_path2(agent, graph, nash,
									simulation.pop_size - simulation.nr_mutated)

		# for generation in simulation.generations:
		#
		# 	for agent in generation.population:
		#
		# 		if not graph.has_node(agent.id) and agent.type != 'mutated':
		#
		# 			graph.add_node(agent.id, colour='grey')

	return graph, pos


def find_path2(agent, graph, nash, pop_size):

	copy_tags = cp.copy(agent.parents)

	for tag in copy_tags:

		if agent.parents[tag].tactic[tag] == nash[tag] and \
		   agent.parents[tag].type != 'mutated':

			if not graph.has_node(agent.parents[tag].id):

				graph.add_node(agent.parents[tag].id, colour='steelblue')

			if not graph.has_edge(agent.parents[tag].id, agent.id):

				graph.add_edge(agent.parents[tag].id, agent.id,
							   colour='steelblue',
							   weight=ses / pop_size)

				if agent.parents[tag].parents != {}:

					graph = find_path2(agent.parents[tag], graph, nash,
									   pop_size)

				del agent.parents[tag]

			else:

				graph[agent.parents[tag].id][agent.id]['weight'] += \
																ses / pop_size
				del agent.parents[tag]

	return graph



def show_network(graph, pos, sizes=None):

	edges, colours_edges = zip(*nx.get_edge_attributes(graph,'colour')\
							   .items())

	nodes, colours_nodes = zip(*nx.get_node_attributes(graph,'colour')\
							   .items())

	summy = 0

	for edge in edges:

		summy += graph[edge[0]][edge[1]]['weight']

	# print(summy)

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


def plot_results(nr_sims, results, type):

	list_hist = {}

	plt.rcParams.update(params)

	for tag in results:

		if tag != 'connectivity' and tag != 'density':

			list_hist[tag] = []
			mean_list = []
			max_list = []

			for sim in results[tag]:

				tmp_list = []

				for pair in sim:

					tmp_list.append(sim[pair])

				list_hist[tag].append(tmp_list)

				mean_list.append(np.mean(tmp_list))

			if type == 'path':
				plt.ylim([0, 200])

			elif type == 'standard':
				plt.ylim(0, 380)

			counts, bins, patches = plt.hist(list_hist[tag], alpha=1)

			plt.gca().set_xticks(bins)
			plt.gca().xaxis.set_major_formatter( \
											mtick.FormatStrFormatter('%0.3f'))

			plt.gca().yaxis.set_major_formatter(mtick.\
										PercentFormatter(xmax=len(tmp_list)))

			# plt.axvline(np.mean(mean_list), color='black', linewidth=1)

			plt.savefig('Results/' + type + '_' + tag + '.png',
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


def save_results(results, type):

	file = open('Results/' + type + '_data.csv', 'w')

	file.write("metric, mean of means, mean of stan dev, stan dev of means, \
				stan dev of stan dev \n")

	for tag in results:

		file.write("%s, " % tag)

		mean_list = []
		std_list = []

		for sim in results[tag]:

			tmp_list = []

			for pair in sim:

				tmp_list.append(sim[pair])

			mean_list.append(np.mean(tmp_list))
			std_list.append(np.std(tmp_list))

		file.write("%s, " % np.mean(mean_list))
		file.write("%s, " % np.mean(std_list))
		file.write("%s, " % np.std(mean_list))
		file.write("%s, " % np.std(std_list))

		file.write("\n")


def save_results2(results, example, type):

	file = open('Results/' + type + '_data3.csv', 'w')

	for tag in results:

		file.write("%s \n " % tag)

		z = 0

		for generation in example.generations:

			file.write("%s, " % z)

			z += 1

		file.write("\n")

		i = 0

		for generation in example.generations:

			gen_list1 = []
			gen_list2 = []

			tag_2 = 1000 * i

			j = 0

			for sim in results[tag]:

				sim_list = []

				k = 0

				for agent in generation.population:

					tag_2 += 1
					k += 1

					if tag_2 in results[tag][j]:

						sim_list.append(results[tag][j][tag_2])

				tag_2 -= k

				gen_list1.append(np.mean(sim_list))
				gen_list2.append(np.std(sim_list))

				j += 1

			i += 1

			file.write("%s; " % np.mean(gen_list1))
			file.write("%s, " % np.mean(gen_list2))

		file.write("\n \n")


def centrality_measures(simulations, nash, type):

	results = {
			   'closeness' : [],
			   'betweenness' : [],
			   'eigenvector' : [],
			   'katz' : [],
			   'degree' : []}
			   # 'connectivity' : [],
			   # 'density' : []}

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
		results['eigenvector'].append(nx.eigenvector_centrality(graph,
												max_iter=1000, weight='weight'))

		# results['connectivity'].append(nx.node_connectivity(graph))
		# results['density'].append(nx.density(graph))

	return results


def values_network(sim, results, type, nash):

	if type == 'standard':

		graph, pos = standard_network2(sim, nash)

	elif type == 'path':

		graph, pos = path_network2(sim, nash)

	for tag in results:

		tmp_list = []

		for pair in results[tag][0]:

			tmp_list.append(results[tag][0][pair])

		max = np.max(tmp_list)

		edges, colours_edges = zip(*nx.get_edge_attributes(graph,'colour')\
									  .items())

		weights = [graph[u][v]['weight'] for u,v in edges]

		nx.draw(graph, pos, node_size=sns, node_color=tmp_list, edgelist=edges,
				arrowstyle='->', arrowsize=1, edge_color='grey',
				width=weights, cmap='plasma_r')

		plt.savefig('Results/' + type + '_' + tag + '_example.png',
					bbox_inches='tight')

		plt.clf()
