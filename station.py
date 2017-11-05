class Station:
	def __init__(self, name, latitude, longitude, critical):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		if critical == "Kritiek":
			self.critical = True
		else:
			self.critical = False

	def __str__(self):
		return (self.name + ", " + str(self.latitude) + ", " + str(self.longitude) + ", "
		+ str(self.critical))
