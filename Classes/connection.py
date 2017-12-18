from Classes.station import Station

class Connection :
	"""Class that contains a connection"""
	def __init__(self, station1, station2, time, critical, index):
		"""Args:
			station1 (String)  : the departure Station
			station2 (String)  : the destination Station
			time (String)	   : the time of the Connection
			critical (String)  : indicates whether a connection is critical
			index (int)		   : unique index of this connection

		  Attributes:
		  	station1 (String)  : the departure Station
			station2 (String)  : the destination Station
			time (int)		   : the time of the Connection
			children (list)    : list with indexnumbers of all possible
								 Connections to go to after this one
			critical (boolean) : indicates whether a connection is critical
			index (int)		   : unique index of this connection
		"""
		self.station1 = station1
		self.station2 = station2
		self.time = int(time)
		self.children = []
		if critical == "TRUE":
			self.critical = True
		else:
			self.critical = False
		self.index = index

	def __str__(self):
		string = (self.station1.name + ", " + self.station2.name + ", "
				  + str(self.time) + str(self.critical))
		return string

	def addChildren(self, connections):
		"""Add children for a connection

		   Args:
		   	connections (list) : list with all Connections
		"""
		for connection in connections:
			if str(connection.station1.name) == str(self.station2.name):
				self.children.append(connection.index)
