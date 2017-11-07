# connection class
# connection == time it takes for a train to get from one station to another
# therefore a connection has two stations and the travel time between them
class Connection:
	def __init__(self, station1, station2, time, critical):
		self.station1 = station1
		self.station2 = station2
		self.time = int(time)

		if critical == "TRUE":
			self.critical = "TRUE"
		else:
			self.critical = "FALSE"

# return all details of a connection
	def __str__(self):
		return (self.station1 + ", " + self.station2 + ", " + str(self.time))