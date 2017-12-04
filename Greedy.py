from Classes.station import Station
from Classes.connection import Connection
from Classes.trajectory import Trajectory

import csv
import random
import itertools

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
		index += 1

# add the children to the connections
for connection in connections:
    connection.addChildren(connections)

critical = []
for connection in connections:
	if connection.critical == True:
		critical.append(connection.index)

reduction = 500

allGreedy = []
for i in range(0, 56):
	Greedy = Trajectory()
	Greedy.createGreedyTrajectory(i, 0, connections)
	allGreedy.append(Greedy)

allCombinations = []
for line in itertools.product(allGreedy, allGreedy, allGreedy, allGreedy):
	allCombinations.append(line)


combinationScores = []
for combination in allCombinations:
	combinationScore = 0
	combinationIndexes = []
	for traject in combination:
		combinationScore = combinationScore + traject.overallScore

		for index in traject.indexes:
			if index in critical:
				if index in combinationIndexes:
						combinationScore = combinationScore - reduction

				elif index % 2 == 0:
					checker = index + 1
					if checker in combinationIndexes:
						combinationScore = combinationScore - reduction

				elif index % 2 == 1:
					checker = index - 1
					if checker in combinationIndexes:
						combinationScore = combinationScore - reduction


		combinationIndexes.extend(traject.indexes)

	combinationScores.append(combinationScore)

print(combinationScores)
print(len(combinationScores))
print(max(combinationScores))

index = combinationScores.index(max(combinationScores))
topCombination = allCombinations[index]

print(topCombination[0])
print(topCombination[1])
print(topCombination[2])
print(topCombination[3])
