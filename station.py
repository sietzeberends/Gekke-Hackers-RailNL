# Class station
# Station has a name, latitude and longitude
# Station can be critical or not

class Station:
	def __init__(self, name, latitude, longitude, critical):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		if critical == "Kritiek":
			self.critical = True
		else:
			self.critical = False

# return all the details of the station
	def __str__(self):
		return (self.name + ", " + str(self.latitude) + ", " + str(self.longitude) + ", "
		+ str(self.critical))
