from __future__ import division
from Classes.station import Station
from Classes.connection import Connection
from Classes.trajectory import Trajectory

import csv
import random
import itertools

def insertIntoDict(name,traject,Dict):
	"""Inserts object into dict.

	   Args:
	   	name (String)        : name of the trajectory
		traject (Trajectory) : Trajectory that is inserted in the dict
		Dict (Dict)          : the Dict where a possible solution is saved

	   Returns: None
	"""
	if not name in Dict:
		Dict[name] = traject
	else:
		Dict[name] = Dict[name] + traject

def replaceDict(content, Dict):
	"""Replaces a combination of Trajectories in the dict

	   Args:
	   	content (Dict) : data to put in the dict
		Dict (Dict)    : dict to put the data in

	   Returns: none
	"""
	Dict.clear()
	Dict.update(content)

def Greedy():
	"""Runs a greedy algorithm on the Holland map"""

	connections = []

	# save all Greedy trajectories
	allGreedy = []

	# hardcoded variables because Greedy only runs on 1 map
	constant = 10000
	totalCritical = 20
	reduction = 50
	totalConnections = 56
	index = 0;

	# load Connections
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

	# create a greedy Trajectory for each connection
	for i in range(0, totalConnections):
		greedy = Trajectory()
		greedy.createGreedyTrajectory(i, 0, connections)
		allGreedy.append(greedy)

	bestScore = 0
	bestCombination = {}

	NumberofRuns = 0

	for combination in itertools.product(allGreedy, allGreedy):

		criticalIndexes = 0
		totalTime = 0
		combinationIndexes = []
		currentCombination = {}
		counter = 0

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
				print("constant: " + str(constant))
				print("criticalIndexes: " + str(criticalIndexes))
				print("totalCritical: " + str(totalCritical))
				print("reduction: " + str(reduction))
				print("len(currentCombination): " + str(len(currentCombination)))
				print("totalTime: " + str(totalTime))
				bestScore = score
				print("New highscore: " + str(bestScore))
				replaceDict(currentCombination, bestCombination)

	print(bestScore)
	print("Number of trajectories: " + str(len(bestCombination)))
