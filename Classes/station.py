from connection import Connection

# Class station
# Station has a name, latitude and longitude
# Station can be critical or not

class Station:
	def __init__(self, name, latitude, longitude, critical, connections):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		self.critical = False;
		if critical == "Kritiek":
			self.critical = True
		self.connections = []

		for connection in connections:
			if connection.station1 == self.name:
				self.connections.append(connection)
			elif connection.station2 == self.name:
				self.connections.append(Connection(connection.station2,
												   connection.station1,
												   connection.time))

# return all the details of the station
	def __str__(self):
		return (self.name + ", " + str(self.latitude) + ", " + str(self.longitude) + ", "
		+ str(self.critical))

	def getConnections(self):

		output = "Station " + self.name + " has the following connections: "

		for connection in self.connections:
			output += connection.station1 + " - " + connection.station2 + " "

		return output
