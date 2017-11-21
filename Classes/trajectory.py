import random
# Class trajectory
# Trajectory has a name and a list of connections

class Trajectory:
	def __init__(self):

		self.connections = []
		self.time = 0
		self.connectionsAmount = 0
		self.indexes = []
		self.bestScores = []

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
		output += " total time: " + str(self.time) + " minutes" + "  Score: " + str(sum(self.bestScores) - 50)
		return output

	# create a random Trajectory
	def createTrajectory(self, index, time, connections):
		connection = connections[index]
		# as long as the Trajectory has a lower duration than 120
		while True:
			if self.time + connection.time <= 120:
				self.connections.append(connection)
				self.indexes.append(connection.index)
				time += connection.time
				self.time = time
			else:
				break
			# if the station only has one child (i.e. is on the edge of civilization)
			if len(connection.children) == 1:
				index = connection.children[0]
			# if the station has more than one child
			else:
				index = random.choice(connection.children)
				# kijk of de connectie al in het traject zit
				while index in self.indexes:
					index = random.choice(connection.children)
					break
			# make sure we don't overstep our constraint
			# recursive
			return self.createTrajectory(index, time, connections)

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
				index = connection.children[0]

			else:
				scores = []
				bestScore = -100

				for child in connection.children:
					placeholder = connections[child]

					if placeholder.critical == True:
						critical = 1
					else:
						critical = 0

					score = (10000 * (critical/22)) - placeholder.time
					scores.append(score)

					if placeholder.station2.name != connection.station1.name:
						if score > bestScore:
							bestScore = score
							index = child

				if index in self.indexes:
					scores.remove(bestScore)
					bestScore = max(scores)
					new_index = scores.index(new_score)
					index = connection.children[new_index]

				self.bestScores.append(bestScore)

			return self.createGreedyTrajectory(index, time, connections)


#pseudo code .

# if connection.critical == True:
	#critical = 1
# else:
	#critical = 0

# score = (10.000 * (critical/22)) - connection.time
