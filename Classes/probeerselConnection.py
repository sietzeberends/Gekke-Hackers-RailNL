from Classes.station import Station

# connection class
# connection == time it takes for a train to get from one station to another
# therefore a connection has two stations and the travel time between them
# connection also contains all possible connections to take next
class Connection :
	def __init__(self, station1, station2, time, critical, index):
		self.station1 = station1
		self.station2 = station2
		self.time = int(time)
		self.connections = []
		self.index = index
		if critical == "TRUE":
			self.critical = "TRUE"
		else:
			self.critical = "FALSE"

# add all the possible connections to go to next
	def addChildren(self, connections):
		for connection in connections:
			if connection.station1.name == self.station1.name:
				print connection.station1.name
				print self.station2.name
				self.connections.append(connection.index)

# return all details of a connection
	def __str__(self):
		return (self.station1.name + ", " + self.station2.name + ", " + str(self.time))
