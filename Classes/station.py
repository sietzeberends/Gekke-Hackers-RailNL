class Station:
	"""Class that contains a station"""
	def __init__(self, name, latitude, longitude, critical):
		"""Args:
			name (String)	   : the name of the Station
			latitude (String)  : the latitude of the Station
			longitude (String) : the longitude of the Station
			critical (String)  : indicates whether a Station is critical

		   Attributes:
		   	name (String)	   : the name of the Station
			latitude (String)  : the latitude of the Station
			longitude (String) : the longitude of the Station
			critical (boolean) : indicates whether a Station is critical
		   """
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		self.critical = False;
		if critical == "Kritiek":
			self.critical = True

	def __str__(self):
		return (self.name + ", " + str(self.latitude) + ", "
		+ str(self.longitude) + ", " + str(self.critical))
