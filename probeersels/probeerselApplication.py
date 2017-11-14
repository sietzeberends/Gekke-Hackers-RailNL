from probeerselStation import Station
from probeerselConnection import Connection
from probeerselTrajectory import Trajectory
from probeerselLijnVoering import LijnVoering
from datetime import datetime

import csv
import random

startTime = datetime.now()

# track all stations and connections in two lists
stations = []
connections = []


# load all the stations
with open('StationsHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		stations.append(Station(row[0], row[1], row[2], row[3]))

# load all the connections
index = 0;
with open('ConnectiesHolland.csv', 'r') as csvfile:
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
		index += 1

# add the children to the connections
for connection in connections:
	connection.addChildren(connections)


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

testLijnVoering = LijnVoering(connections)
highScore = 0
aantalLijnvoeringen = 0
while highScore < 10000:
	aantalLijnvoeringen += 1
	testLijnVoering = LijnVoering(connections)
	testLijnVoering.createRandomLineFeeding(testLijnVoering.trajectories)
	highScore = testLijnVoering.LineFeedingScore()


print(testLijnVoering)
print("Score: " + str(highScore))
print("Aantal Lijnvoeringen voor bereiken maximale score: " + str(aantalLijnvoeringen))


# testTrajectory.createTrajectory(firstConnectionIndex, time, connections)
# print (testTrajectory)

timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))
