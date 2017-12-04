import random
# Class trajectory
# Trajectory has a name and a list of connections

class Trajectory:
	def __init__(self):

		self.connections = []
		self.time = 0
		self.connectionsAmount = 0
		self.indexes = []
		self.overallScore = - 50

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
		output += " total time: " + str(self.time) + " minutes" + "  Score: " + str(self.overallScore)
		return output

	# create a random Trajectory
	def createTrajectory(self, index, time, connections, maxMinutes):

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

			# if the station only has one child
			# i.e. is on the edge of civilization
			# then go back where you came from
			if len(connection.children) == 1:
				index = connection.children[0]

			# if the station has more than one child
			# pick where to go next (random)
			else:
				index = random.choice(connection.children)
				if len(self.indexes) != 0:
					stopcounter = 0
					while connections[index].station2.name == connection.station1.name:
						# print("trein vertrekt van :" + connection.station1.name)
						# print("trein komt aan in :" + connection.station2.name)
						# print("trein van: " + connections[index].station1.name)
						# print("mag niet aankomen op : " + connection.station1.name)
						# print("de nieuwe connecties waar we uit kunnen kiezen zijn: ")
						# for index in connection.children:
							# print(str(connections[index]))
						index = random.choice(connection.children)
						# print("gekozen connectie: " + str(connections[index]))
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

				self.overallScore += bestScore

			return self.createGreedyTrajectory(newIndex, time, connections)
>>>>>>> 858d8a2dc9c985be4524ae69bfd272d24f9a7314
