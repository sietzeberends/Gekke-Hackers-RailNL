from Classes.station import Station
from Classes.connection import Connection
from Classes.trajectory import Trajectory
from Classes.lijnvoering import LijnVoering

import csv
import random

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

allGreedy = []
for i in range(0, 56):
	Greedy = Trajectory()
	Greedy.createGreedyTrajectory(i, 0, connections)
	allGreedy.append(Greedy)

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
