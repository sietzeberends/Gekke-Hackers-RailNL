from station import Station
from connection import Connection
import csv

# track all stations and connections in two lists
stations = []
connections = []

# load all the stations
with open('StationsHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		stations.append(Station(row[0], row[1], row[2], row[3]))

# load all the connections
with open('ConnectiesHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		connections.append(Connection(row[0], row[1], row[2]))

# print stations and connections to check if they loaded succesfully
for station in stations:
	print str(station)

for connection in connections:
	print str(connection)