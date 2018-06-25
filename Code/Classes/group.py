

class Group(object):

	def __init__(self, id, generation_nr, tactic, generation):

		self.id = id
		self.gen = generation_nr
		self.tactic = tactic

		self.population = self.find_population(generation)
		self.parents = None


	def find_population(self, generation):

		population = []

		for agent in generation.population:

			if agent.tactic == self.tactic:

				population.append(agent)

		return population


	def find_parents(self, generation):

		self.parents = {}

		for tag_2 in generation.groups:

			self.parents[tag_2] = 0

			for agent in self.population:

				for tag in agent.parents:

					if agent.parents[tag].tactic == \
					   generation.groups[tag_2].tactic:

						self.parents[tag_2] += 1
