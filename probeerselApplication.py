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
index = 0;
with open('csvFiles/ConnectiesHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		connections.append(Connection(Station(row[0], "", "", row[3]),
									  Station(row[1], "", "", row[3]),
									  row[2],
									  row[3], index))
		index += 1
		connections.append(Connection(Station(row[1], "", "", row[3]),
									  Station(row[0], "", "", row[3]),
									  row[2],
									  row[3], index))

# add the children to the connections
for connection in connections:
	connection.addChildren(connections)

print connections[1]
for child in connections[1].connections:
	print connections[child].station1.name
	print connections[child].station2.name


count = 0
stationsk = []
for connection in connections:
	if connection.critical == "TRUE":
	  stationsk.append(connection.station1.name)
	  stationsk.append(connection.station2.name)
for Station.name in stations:
	if str(Station.name) in stationsk:
		count += 1
		print (count)
if count == 22:
	print ("POOF IT IS PROOF QED")
else:
	print ("not a PROOF")


testTrajectory = Trajectory([])
time = 0
firstConnectionIndex = random.choice(connections).index
print "first: " + str(firstConnectionIndex)
testTrajectory.createTrajectory(firstConnectionIndex, time, connections)
timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))
for connection in testTrajectory.connections:
	print connection.station1.name + " - " + connection.station2.name
