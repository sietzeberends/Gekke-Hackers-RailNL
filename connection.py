class Connection:
	def __init__(self, station1, station2, time):
		self.station1 = station1
		self.station2 = station2
		self.time = time

	def __str__(self):
		return (self.station1 + ", " + self.station2 + ", " + str(self.time))
