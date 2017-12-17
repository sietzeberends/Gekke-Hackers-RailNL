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


# define variables for scorefunction
constant = 10000
totalCritical = 21
reduction = 50
totalConnections = 56

def Greedy():

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

	# save all Greedy trajectories
	allGreedy = []

	for i in range(0, totalConnections):
		Greedy = Trajectory()
		Greedy.createGreedyTrajectory(i, 0, connections)
		allGreedy.append(Greedy)

	bestScore = 0
	bestCombination = {}

	def insertIntoDict(name,traject,Dict):
	    if not name in Dict:
	        Dict[name] = traject
	    else:
	        Dict[name] = Dict[name] + traject

	def replaceDict(content, Dict):
		Dict.clear()
		Dict.update(content)

	for combination in itertools.product(allGreedy, allGreedy, allGreedy):

		criticalIndexes = 0
		totalTime = 0
		combinationIndexes = []
		currentCombination = {}
		counter = 0
		testBroertjes = 0

		for traject in combination:
			totalTime = totalTime + traject.time
			insertIntoDict("traject" + str(counter), traject, currentCombination)
			counter = counter + 1

			for connection in traject.connections:
				if connection.critical == True:
					if connection.index in combinationIndexes:
						continue
					check = connection.index % 2
					if check == 0:
						check = connection.index + 1
						if check in combinationIndexes:
							continue
					if check == 1:
						check = connection.index - 1
						if check in combinationIndexes:
							continue

					criticalIndexes = criticalIndexes + 1

			combinationIndexes = combinationIndexes + traject.indexes

			score = constant * (criticalIndexes/totalCritical) - (reduction * len(currentCombination)) - totalTime

			if score > bestScore:
				bestScore = score
				replaceDict(currentCombination, bestCombination)

	print(bestScore)
	print("Number of trajectories: " + str(len(bestCombination)))

Greedy()
