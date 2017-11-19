from Classes.connection import Connection
from Classes.station import Station
import csv

stations = []
connections = []

class writetocsv:

	def __init___(self, outfile, connection):
		self.connection = connection.station1.name + ", " +
		 			      connection.station2.name + ", " +
						  str(connection.time)

		self.connection_seperated = self.connection.split(",")

		with open (outfile, "w") as outfile:
			writer = csv.writer(outfile, dialect='excel')
			writer.writerow(self.connection_seperated)
