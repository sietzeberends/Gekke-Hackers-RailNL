from Classes.station import Station
from Classes.connection import Connection
from Classes.trajectory import Trajectory
from datetime import datetime

import csv
import random

# track all stations and connections in two lists
stations = []
connections = []

# load all the connections
with open('csvFiles/ConnectiesHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		connections.append(Connection(row[0], row[1], row[2]))

for connection in connections:
    print connection

# load all the stations
with open('csvFiles/StationsHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		stations.append(Station(row[0], row[1], row[2], row[3], connections))

for station in stations:
    print station

startTime = datetime.now()

def addconnection():
    connectionsForFirstTrajectory.append(random.choice(connections))
    while len(connectionsForFirstTrajectory) < 5:
        x = random.choice(connections)
        if x.station1 == connectionsForFirstTrajectory[-1].station2:
          connectionsForFirstTrajectory.append(x)

addconnection()
print stations[0].getConnections()

firstTrajectory = Trajectory(connectionsForFirstTrajectory)

timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))


# let's test if our connections can be put in an instance of the class 'Trajectory'
connectionsForFirstTrajectory = []

# we use connections to create a trajectory between Amsterdam Amstel and Haarlem
# TODO: create a function to generate a random traject
# of course, connections need to be linked to eachother
connectionsForFirstTrajectory.extend((connections[2], connections[7], connections[6]))

# now, let's build the first trajectory. Right now, the name is manually given
# TODO: create a function to create the name of the trajectory
# based on the first station of the first connection in the trajectory
# and the last station of the last connection in the trajectory
firstTrajectory = Trajectory("Amsterdam Amstel -> Haarlem", connectionsForFirstTrajectory)

# check if it worked
print firstTrajectory
