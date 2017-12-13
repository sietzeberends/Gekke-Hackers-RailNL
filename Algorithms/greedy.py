from __future__ import division
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


combinationScores = []
allCombinations = {}
counter = 0
allScores = []

def insertIntoDict(name,traject,Dict):
    if not name in Dict:
        Dict[name] = traject.indexes
    else:
        Dict[name] = Dict[name] + traject.indexes

amountCritical = []

for combination in itertools.product(allGreedy, allGreedy, allGreedy, allGreedy):

	combinationIndexes = []
	criticalIndexes = 0
	totalTime = 0

	for traject in combination:
		insertIntoDict("combination" + str(counter),traject,allCombinations)
		totalTime = totalTime + traject.time

	currentCombination = allCombinations["combination" + str(counter)]

	for index in currentCombination:
		if index in critical:
			if index in combinationIndexes:
				continue
			elif index % 2 == 0:
				checker = index + 1
				if checker in combinationIndexes:
					continue
			elif index % 2 == 1:
				checker = index - 1
				if checker in combinationIndexes:
					continue

			criticalIndexes = criticalIndexes + 1

		combinationIndexes.append(index)
	score = 10000 * (criticalIndexes/20) - (50 * len(currentCombination)) - totalTime
	allScores.append(score)
	counter = counter + 1
	amountCritical.append(criticalIndexes)

print(len(allCombinations))
print(max(allScores))

indexTop = allScores.index(max(allScores))

indexesTop = allCombinations["combination" + str(indexTop)]

for index in indexesTop:
	print(connections[index])

print("Amount of critical connections =" + str(amountCritical[indexTop]))
