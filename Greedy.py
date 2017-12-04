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

<<<<<<< HEAD
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
=======
allScores = []
combinations = []

for first_traject in allGreedy:
	for second_traject in allGreedy:
		for third_traject in allGreedy:
			for fourth_traject in allGreedy:
				combinedScore = first_traject.overallScore +\
								second_traject.overallScore +\
								third_traject.overallScore +\
								fourth_traject.overallScore

		for index in first_traject.indexes:
			if index in second_traject.indexes or third_traject.indexes or fourth_traject.indexes:
				combinedScore = combinedScore - 450

			check = index % 2
			if check == 0:
				checker = index + 1
				if checker in second_traject.indexes:
					combinedScore = combinedScore - 450
			if check == 1:
				checker = index - 1
				if checker in second_traject.indexes:
					combinedScore = combinedScore - 450


		for index in second_traject.indexes:
			if index in third_traject.indexes or fourth_traject.indexes:
				combinedScore = combinedScore - 450

			check = index % 2
			if check == 0:
				checker = index + 1
				if checker in third_traject.indexes or fourth_traject.indexes:
					combinedScore = combinedScore - 450
			if check == 1:
				checker = index - 1
				if checker in third_traject.indexes or fourth_traject.indexes:
					combinedScore = combinedScore - 450

		for index in third_traject.indexes:
			if index in fourth_traject.indexes:
				combinedScore = combinedScore - 450

			check = index % 2
			if check == 0:
				checker = index + 1
				if checker in fourth_traject.indexes:
					combinedScore = combinedScore - 450
			if check == 1:
				checker = index - 1
				if checker in fourth_traject.indexes:
					combinedScore = combinedScore - 450

		allScores.append(combinedScore)
		combinations.append([first_traject, second_traject, third_traject, fourth_traject])

bestScore = max(allScores)
print(bestScore)
indexScore = allScores.index(bestScore)

test = combinations[indexScore]
print(test[0])
print(test[1])
print(test[2])
print(test[3])
>>>>>>> 858d8a2dc9c985be4524ae69bfd272d24f9a7314
