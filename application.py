from Classes.station import Station
from Classes.connection import Connection
from Classes.trajectory import Trajectory
from Classes.lijnvoering import LijnVoering
from datetime import datetime

import csv
import random
import sys



def loadStations(csvFilepath):
	"""Load stations from a CSV file and returns them as a list"""

	stationsList = []
	with open(csvFilepath, 'r') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
			stationsList.append(Station(row[0], row[1], row[2], row[3]))

	return stationsList

def loadConnections(csvFilepath):
	"""Loads connections from a CSV file and returns them as a list"""

	connectionsList = []
	index = 0;
	with open(csvFilepath, 'r') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
			connectionsList.append(Connection(Station(row[0], "", "", row[3]),
										  Station(row[1], "", "", row[3]),
										  row[2],
										  row[3], index))

			index += 1
			connectionsList.append(Connection(Station(row[1], "", "", row[3]),
										  Station(row[0], "", "", row[3]),
										  row[2],
										  row[3], index))
			index += 1

	# add the children to the connections and count how many connections are critical
	for connection in connectionsList:
		connection.addChildren(connectionsList)

	return connectionsList

def minutesPerTrajectory(connections):
	"""Calculates the allowed amount of minutes per trajectory and returns that number"""
	minutes = 0
	if len(connections) <= 28:
		minutes = 120
	else:
		minutes = 180

	return minutes


# track how long the application runs
startTime = datetime.now()

# track all stations and connections in two lists
stations = loadStations('csvFiles/StationsNationaal.csv')
connections = loadConnections('csvFiles/ConnectiesNationaal.csv')

highScore = 0
besteLijnvoering = LijnVoering(connections)
testHillClimber = LijnVoering(connections)

for i in range(1,100):
	print("run: " + str(i))
	testHillClimber = LijnVoering(connections)
	for i in range(1,21):
		hillClimberScore = testHillClimber.hillClimber(testHillClimber.trajectories, connections, i)
		print(str(i) + " trajecten")
		print("highScore tot nu toe: " + str(highScore))
		# testHillClimber.createRandomLijnVoering(testHillClimber.trajectories)
		if(highScore < hillClimberScore):
			besteLijnvoering.trajectories.clear()
			besteLijnvoering.time = 0
			aantalkritiek = 0
			for trajectory in testHillClimber.trajectories:
				besteLijnvoering.trajectories.append(trajectory)
				besteLijnvoering.time += trajectory.time
				for connection in trajectory.connections:
					if connection.critical == True:
						aantalkritiek += 1
			aantalkritiek /= 2
			highScore = hillClimberScore
			print(testHillClimber)
			print ("Nieuwe highscore: " + str(highScore))
			print ("Totale tijd van lijnvoering: " + str(besteLijnvoering.time))
			print ("Aantal kritiek: " + str(aantalkritiek))


			with open ("csvFiles/connections_visualisation.csv", "w") as outfile:
				writer = csv.writer(outfile, dialect='excel')
				for trajectory in besteLijnvoering.trajectories:
					writer.writerow("-")
					for connection in trajectory.connections:
						placeholder = connection.station1.name + ", " +\
		 			  				  connection.station2.name + ", " +\
				      				  str(connection.time)
						placeholder = placeholder.split(",")
						writer.writerow(placeholder)
			with open ("dataPlot.csv", "a", newline="") as outfile:
				writer = csv.writer(outfile, dialect="excel")
				placeholder1 = 		str(len(besteLijnvoering.trajectories)) + ", " +\
									str(hillClimberScore) + ", " +\
									str(besteLijnvoering.time)
				placeholder1 = placeholder1.split(",")
				writer.writerow(placeholder1)

print("Beste lijnvoering " + str(len(besteLijnvoering.trajectories)) + ": " + str(highScore))
print(str(besteLijnvoering))
print ("Totale tijd van lijnvoering: " + str(besteLijnvoering.time))

# print the runtime
timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))
