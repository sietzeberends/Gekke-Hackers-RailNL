from Classes.connection import Connection
from Classes.station import Station


import csv

stations = []
connections = []

with open('csvFiles/StationsHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile, delimiter=";")
	for row in rows:
		stations.append(Station(row[0], row[1], row[2], row[3]))
		

with open('csvFiles/ConnectiesHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		connections.append(Connection(Station(row[0], "", "", row[3]), Station(row[1], "", "", row[3]), row[2],row[3]))


test = connections[0].station1.name + ", " + connections[0].station2.name + ", " + str(connections[0].time)

test_1 = test.split(",")

print(test_1)

with open ("csvFiles/test_connection.csv", "w") as outfile:
	writer = csv.writer(outfile, dialect='excel')
	writer.writerow(test_1)
	

