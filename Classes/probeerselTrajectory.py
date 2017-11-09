import random
# Class trajectory
# Trajectory has a name and a list of connections

class Trajectory:
	def __init__(self, connections):

		self.connections = connections
		self.time = 0
		self.connectionsAmount = 0;

		for connection in connections:
			self.time += connection.time
			connections.amount += 1;

	# return all the information about a Trajectory
	def __str__(self):
		output = ""
		for connection in self.connections:
			 output += connection.station1.name
			 output += " -> "

		output += " total time: " + str(self.time) + " minutes"
		return output

	# create a random Trajectory
	def createTrajectory(self, index, time, connections):
		connection = connections[index]
		# as long as the Trajectory has a lower duration than 120
		while True:
			if self.time + connection.time < 120:
				self.connections.append(connection)
				time += connection.time
				self.time = time
			else:
				break
			# if the station only has one child (i.e. is on the edge of civilization)
			if len(connection.connections) == 1:
				index = connection.connections[0]
			# if the station has more than one child
			else:
				index = random.choice(connection.connections)
				print index
			# make sure we don't overstep our constraint
			# recursive
			return self.createTrajectory(index, time, connections)
