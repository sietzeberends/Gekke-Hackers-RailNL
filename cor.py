from itertools import product
import csv

stations = dict()

# loop over the Stations and save the coordinates in two lists
with open('StationsHolland.csv', 'r') as csvfile:
	rows = csv.reader(csvfile, delimiter=',')
	for row in rows: 
		stations[row[0]] = row[1], row[2]
		
		
# ws = file('StationsHolland.csv','r',1)


for x in stations:
	print(x)
<<<<<<< HEAD
	for y in stationsx]:
		print(stations[x])

asdasdasdasjhvsdf

floris is een lul
=======
	for y in stations[x]:
		print(stations[x])

print("Je boy is hier")
>>>>>>> 1b638df84a054974fa63aa3d7af58e400595d4c9
