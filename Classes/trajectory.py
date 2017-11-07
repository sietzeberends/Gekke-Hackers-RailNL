# Class trajectory
# Trajectory has a name and a list of connections

class Trajectory:
	def __init__(self, name, connections):
		self.name = name
		self.connections = connections

	def __str__(self):
		output = ""
		time = 0
		for connection in self.connections:
			 output += connection.station1
			 output += " - "
			 output += connection.station2
			 output += "; "
			 time += connection.time

		output += "total time: " + str(time) + " minutes"
		return output
