

import matplotlib.pyplot as plt


def create_lists(simulation):

	info = {'u + r' : [],
			'u + b' : [],
			'r + r' : [],
			'r + b' : [],
			'b + r' : [],
			'b + b' : []}

	for generation in simulation.generations:

		sums = {'u + r' : 0,
				'u + b' : 0,
				'r + r' : 0,
				'r + b' : 0,
				'b + r' : 0,
				'b + b' : 0}

		pop_size = len(generation.population)

		for agent in generation.population:

			sums['u + r'] += agent.tactic['unknown']['red'] / pop_size
			sums['u + b'] += agent.tactic['unknown']['black'] / pop_size
			sums['r + r'] += agent.tactic['red']['red'] / pop_size
			sums['r + b'] += agent.tactic['red']['black'] / pop_size
			sums['b + r'] += agent.tactic['black']['red'] / pop_size
			sums['b + b'] += agent.tactic['black']['black'] / pop_size

		for phenotype in info:

			info[phenotype].append(sums[phenotype])

	return info


def plot_results(info):

	fig = plt.figure(1)

	ax1 = fig.add_subplot(231)
	ax2 = fig.add_subplot(232)
	ax3 = fig.add_subplot(233)
	ax4 = fig.add_subplot(234)
	ax5 = fig.add_subplot(235)
	ax6 = fig.add_subplot(236)

	ax1.plot(info['u + r'])
	ax4.plot(info['u + b'])
	ax2.plot(info['r + r'])
	ax5.plot(info['r + b'])
	ax3.plot(info['b + r'])
	ax6.plot(info['b + b'])


	plt.show()
