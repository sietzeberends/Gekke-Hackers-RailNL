from station import Station
from connection import Connection
from trajectory import Trajectory
from datetime import datetime

import random
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
# y = random.choice(connections)
# def addconnection(y):
# 	y = random.choice(connections)
# 	if len(connectionsForFirstTrajectory) > 10:
# 		return connectionsForFirstTrajectory
# 	else:
# 		for connection in connections:
# 			if connection.station2 == y.station1:
# 				return addconnection(connectionsForFirstTrajectory.extend((connection, y)))

# store time
startTime = datetime.now()

def addconnection():
    connectionsForFirstTrajectory.append(random.choice(connections))
    while len(connectionsForFirstTrajectory) < 5:
        x = random.choice(connections)
        if x.station1 == connectionsForFirstTrajectory[-1].station2:
          connectionsForFirstTrajectory.append(x)

# while connectionsForFirstTrajectory[7] == False:
addconnection()
#
# for connection in connections:
# 	x = random.choice(connections)
# 	if (y.station2 == x.station1 and y.time < (120 - x.time)):
# 		connectionsForFirstTrajectory.extend((y, x))

# now, let's build the first trajectory. Right now, the name is manually given
# TODO: create a function to create the name of the trajectory
# based on the first station of the first connection in the trajectory
# and the last station of the last connection in the trajectory
firstTrajectory = Trajectory(connectionsForFirstTrajectory)

timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))

# check if it worked
print firstTrajectory
