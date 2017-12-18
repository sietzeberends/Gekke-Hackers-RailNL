import random

class Trajectory:
	"""Class that contains a trajectory, which exists of connections"""
	def __init__(self):
		"""Attributes:
			connections (list)      : list with all Connections in this
									  Trajectory
			time (int)				: the sum of the time of all Connections in
									  this Trajectory
			connectionsAmount (int)	: the amount of Connections in this
									  Trajectory
			indexes (list)			: the indexes of Connections in this
									  Trajectory
		"""

		self.connections = []
		self.time = 0
		self.connectionsAmount = 0
		self.indexes = []

		for connection in self.connections:
			self.time += connection.time
			self.connectionsAmount += 1;

	def __str__(self):
		output = ""
		for connection in self.connections:
			output += connection.station1.name
			output += " -> "

		last_station = self.connections[-1]
		output += last_station.station2.name
		output += " total time: " + str(self.time) + " minutes"
		return output

	def createTrajectory(self, index, time, connections, maxMinutes):
		"""Creates a random Trajectory

		   Args:
		   	index (int)        : index of the starting Connection
			time (int)		   : total time of the Trajectory
			connections (list) : list with all Connections
			maxMinutes (int)   : maximum amount of minutes that is allowed
								 for this Trajectory
		   Returns: Trajectory
		"""
		connection = connections[index]
		# as long as the Trajectory has a lower duration than 120 minutes
		while True:
			if self.time + connection.time <= maxMinutes:
				self.connections.append(connection)
				if index % 2 == 0:
					self.indexes.append(connection.index)
				time += connection.time
				self.time = time
			else:
				break

			# if the station only has one child (edge of the map)
			if len(connection.children) == 1:
				index = connection.children[0]

			# if the station has more than one child
			else:
				index = random.choice(connection.children)
				if len(self.indexes) != 0:
					stopcounter = 0
					while (connections[index].station2.name ==
					       connection.station1.name):
						index = random.choice(connection.children)
						stopcounter += 1
						if stopcounter > 10000:
							print("we geven het op")
							break
			# recursive
			return self.createTrajectory(index, time, connections, maxMinutes)

	def createGreedyTrajectory(self, index, time, connections):

		connection = connections[index]

		while True:
			if self.time + connection.time <= 120:
				self.connections.append(connection)
				self.indexes.append(connection.index)
				time += connection.time
				self.time = time
			else:
				break

			if len(connection.children) == 1:
				newIndex = connection.children[0]

			else:

				newIndex = None
				scores = []
				children = []

				for child in connection.children:
					placeholder = connections[child]

					if placeholder.station2.name == connection.station1.name:
						continue

					elif placeholder.index in self.indexes:
						continue

					check = placeholder.index % 2
					if check == 0:
						checker = placeholder.index + 1
						if checker in self.indexes:
							continue
					if check == 1:
						checker = placeholder.index - 1
						if checker in self.indexes:
							continue

					score = None

					if placeholder.critical == True:
						score = 500 - placeholder.time
					else:
						score = 0 - placeholder.time

					scores.append(score)
					children.append(placeholder.index)

				if not scores:
					break

				bestScore = max(scores)

				indexScore = scores.index(bestScore)
				newIndex = children[indexScore]

			return self.createGreedyTrajectory(newIndex, time, connections)
