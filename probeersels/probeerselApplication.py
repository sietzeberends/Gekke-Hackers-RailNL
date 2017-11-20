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

# testLijnVoering = LijnVoering(connections)
# highScoreA = 0
# aantalLijnvoeringen = 0
# while highScoreA < 10000:
# 	aantalLijnvoeringen += 1
# 	testLijnVoering = LijnVoering(connections)
# 	testLijnVoering.createRandomLijnVoering(testLijnVoering.trajectories)
# 	highScoreA = testLijnVoering.ScoreOpdrachtA()
# 	print(highScoreA)

highScore = 0
aantalTrajectenBeste = 0
besteLijnvoering = LijnVoering(connections)

# voer de hillCLimber 100 keer uit
for j in range(1,100):
	print("run: " + str(j))
	testHillClimber = LijnVoering(connections)
	for i in range(1,8):
		hillClimberScore = testHillClimber.hillClimber(testHillClimber.trajectories, connections, i)
		print(str(i) + " trajecten")
		# testHillClimber.createRandomLijnVoering(testHillClimber.trajectories)
		if(highScore < hillClimberScore):
			print(highScore)
			print(hillClimberScore)
			highScore = hillClimberScore
			aantalTrajectenBeste = i
			besteLijnvoering.trajectories.clear()
			for trajectory in testHillClimber.trajectories:
				besteLijnvoering.trajectories.append(trajectory)
			print(str(besteLijnvoering))



print("Traject " + str(aantalTrajectenBeste) + ": " + str(highScore))
print(str(besteLijnvoering))
print(besteLijnvoering.scoreOpdrachtB)

# for trajectory in testHillClimber.trajectories:
# 	for connection in trajectory.connections:
# 		print(connection)



# print(testLijnVoering)
# print("Score: " + str(highScoreA))
# print("Aantal Lijnvoeringen voor bereiken maximale score: " + str(aantalLijnvoeringen))

#breadthLijnvoering = LijnVoering(connections)
#print(breadthLijnvoering.createAllPossibleLijnVoeringen(connections, 0, 0, ""))


# testLijnVoering.queue(connections)
# testTrajectory.createTrajectory(firstConnectionIndex, time, connections)
# print (testTrajectory)

timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))
