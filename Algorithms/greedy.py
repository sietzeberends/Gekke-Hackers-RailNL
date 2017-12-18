import math
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

	# store best score and combination
	bestScore = 0
	bestCombination = {}

	# we always run the greedy for 4 trajectories
	for combination in itertools.product(allGreedy, allGreedy, allGreedy,
										 allGreedy):

		# variables for scorefunction
		criticalIndexes = 0
		totalTime = 0

		# stores current combination
		# stores previous critical connections
		combinationCritical = []
		currentCombination = {}

		counter = 0

		# loop through trajectory in a combination
		for traject in combination:
			totalTime = totalTime + traject.time
			insertIntoDict("traject" + str(counter), traject, currentCombination)
			counter = counter + 1

			# check each connection in the trajectory
			for connection in traject.connections:
				if connection.critical == True:

					# ensure no critical connection is counted twice
					if connection.index in combinationCritical:
						continue

					# ensure connection in opposite direction isn't counted twice
					check = connection.index % 2
					if check == 0:
						check = connection.index + 1
						if check in combinationCritical:
							continue
					if check == 1:
						check = connection.index - 1
						if check in combinationCritical:
							continue

					# count a (new) critical connection
					criticalIndexes = criticalIndexes + 1

					# save critical connection as passed
					combinationCritical.append(connection.index)

			# calculate score for a combination
			score = constant * (criticalIndexes/totalCritical) - (reduction * len(currentCombination)) - totalTime

			# if score of combination is higher than highscore, save score
			if score > bestScore:
				bestScore = score
				replaceDict(currentCombination, bestCombination)
				print("New highscore: " + str(bestScore))

	# when done, print the highest score
	print("Overall highscore: " + str(bestScore))
