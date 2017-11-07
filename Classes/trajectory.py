# Class trajectory
# Trajectory has a name and a list of connections

class Trajectory:
	def __init__(self, connections):

		self.connections = connections
		self.time = 0
		
		for connection in connections:
			self.time += connection.time

	def __str__(self):
		output = ""
		time = 0
		for connection in self.connections:
			 output += connection.station1
			 output += " -> "

		last_station = self.connections[-1]
		output += last_station.station2

		output += " total time: " + str(self.time) + " minutes"
		return output
