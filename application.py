from Classes.station import Station
from Classes.connection import Connection
from Classes.trajectory import Trajectory
from datetime import datetime

import csv
import random

startTime = datetime.now()

# track all stations and connections in two lists
stations = []
connections = []


# load all the stations
with open('csvFiles/StationsHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		stations.append(Station(row[0], row[1], row[2], row[3]))

# load all the connections
with open('csvFiles/ConnectiesHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		connections.append(Connection(Station(row[0], "", "", row[3]),
									  Station(row[1], "", "", row[3]),
									  row[2],
									  row[3]))
# add the children to the connections
for connection in connections:
	connection.addChildren(connections)

# stationsk = []
# for connection in connections:
#   if connection.critical == True:
#     stationsk.append(connection.station1, connection.station2)
# for station in stations:
#     if (station == stations.index(stationsk[0])) or (station == stations.index(stationsk[1])):
#       count += 1
#     else:
#       print "not proven"
#     if count == 22:
#       print "POOF IT IS PROOF"

connectionsForTrajectory =[]

# create a random Trajectory
def createTrajectory(connection, time):
	connectionsForTrajectory.append(connection)
	time += connection.time
	# as long as the Trajectory has a lower duration than 120
	while True:
		# if the station only has one child (i.e. is on the edge of civilization)
		if len(connection.connections) == 1:
			newConnection = connection.connections[0]
			newConnection.addChildren(connections)
		# if the station has more than one child
		else:
			newConnection = random.choice(connection.connections[0:-1])
			newConnection.addChildren(connections)
		# make sure we don't overstep our constraint
		if newConnection.time + time < 120:
			# recursive
			return createTrajectory(newConnection, time)
		else:
			break

time = 0
createTrajectory(random.choice(connections), time)

# startTime.sleep(5)

timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))

firstTrajectory = Trajectory(connectionsForTrajectory)

# check if it worked
print firstTrajectory
