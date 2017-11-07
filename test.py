from station import Station
from connection import Connection
from trajectory import Trajectory

import csv

# track all stations and connections in two lists
stations = []
connections = []

# load all the connections
with open('ConnectiesHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		connections.append(Connection(row[0], row[1], row[2]))

for connection in connections:
    print connection

# load all the stations
with open('StationsHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		stations.append(Station(row[0], row[1], row[2], row[3], connections))

for station in stations:
    print station

print stations[0].getConnections()
