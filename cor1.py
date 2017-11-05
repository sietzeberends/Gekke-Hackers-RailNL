import product
import csv

stations = dict()
connections = {}
# loop over the Stations and save the coordinates in two lists
with open('StationsHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile, delimiter=',')
	for row in rows:
		stations[row[0]] = row[1], row[2]

with open('ConnectiesHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		connectionsname = ""
		connectionsname += row[0] + ' -> ' + row[1]
		connections[connectionsname] = row[2]

for connection in connections:
	print connection, connections[connection]

for x in stations:
	print x, stations[x]

for connections in traject:
	total += connections[connections][1]

connection = connections[1]
total = 0

while total <= 120:
  traject.append(connections[1])
  total += 1
