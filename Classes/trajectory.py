import random
# Class trajectory
# Trajectory has a name and a list of connections

class Trajectory:
	def __init__(self):

		self.connections = []
		self.time = 0
		self.connectionsAmount = 0;
		self.indexes = []

		for connection in self.connections:
			self.time += connection.time
			self.connectionsAmount += 1;

	# return all the information about a Trajectory
	def __str__(self):
		output = ""
		for connection in self.connections:
			output += connection.station1.name
			output += " -> "

		last_station = self.connections[-1]
		output += last_station.station2.name
		output += " total time: " + str(self.time) + " minutes"
		return output

	# create a random Trajectory
	def createTrajectory(self, index, time, connections):
		connection = connections[index]

		# as long as the Trajectory has a lower duration than 120 minutes
		while True:
			if self.time + connection.time <= 120:
				self.connections.append(connection)
				self.indexes.append(connection.index)
				time += connection.time
				self.time = time
			else:
				break

			# if the station only has one child
			# i.e. is on the edge of civilization
			# then go back where you came from
			if len(connection.children) == 1:
				index = connection.children[0]

			# if the station has more than one child
			# pick where to go next (random)
			else:
				index = random.choice(connection.children)

				# check if the connections is already in the trajectory
				# if so, break
				while index in self.indexes:
					index = random.choice(connection.children)
					break

			# recursive
			return self.createTrajectory(index, time, connections)
