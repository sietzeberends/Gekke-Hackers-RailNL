from station import Station
from connection import Connection
from trajectory import Trajectory

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

# let's test if our connections can be put in an instance of the class 'Trajectory'
connectionsForFirstTrajectory = []

# we use connections to create a trajectory between Amsterdam Amstel and Haarlem
# TODO: create a function to generate a random traject
# of course, connections need to be linked to eachother
connectionsForFirstTrajectory.extend((connections[2], connections[7], connections[6]))

# now, let's build the first trajectory. Right now, the name is manually given
# TODO: create a function to create the name of the trajectory
# based on the first station of the first connection in the trajectory
# and the last station of the last connection in the trajectory
firstTrajectory = Trajectory("Amsterdam Amstel -> Haarlem", connectionsForFirstTrajectory)

# check if it worked
print firstTrajectory
