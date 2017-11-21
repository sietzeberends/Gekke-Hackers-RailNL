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

save_scores_traject1 = []
# check all starter stations
for i in range(0,56):
    greed = Trajectory()
    greed.createGreedyTrajectory(i, 0, connections)
    score = sum(greed.bestScores) - 50
    save_scores_traject1.append(score)

# highest score for a single trajectory
print(max(save_scores_traject1))
