from Classes.station import Station
from Classes.connection import Connection
from Classes.trajectory import Trajectory
from Classes.lijnvoering import LijnVoering
from datetime import datetime

import csv
import random
import sys

# track how long the application runs
startTime = datetime.now()

# highScore = 0
#
# for i in range(1,1000):
# 	print("run: " + str(i))
# 	testHillClimber = LijnVoering('csvFiles/ConnectiesHolland.csv')
# 	besteLijnvoering = testHillClimber.hillClimber()
# 	if besteLijnvoering.scoreOpdrachtB() > highScore:
# 		print("highScore tot nu toe: " + str(highScore))
# 		highScore = besteLijnvoering.scoreOpdrachtB()
# 		print(str(i) + " trajecten")
# 		print(besteLijnvoering)
# 		print ("Nieuwe highscore: " + str(highScore))
# 		print ("Totale tijd van lijnvoering: " + str(besteLijnvoering.time))
# 		print ("Aantal kritieke trajecten: " + str(besteLijnvoering.kritiekInLijnvoering))
# 		print ("deler: " + str(besteLijnvoering.kritiekTotaal))
#
# print("Beste lijnvoering " + str(len(besteLijnvoering.trajectories)) + ": " + str(highScore))
# print(str(besteLijnvoering))
# print ("Totale tijd van lijnvoering: " + str(besteLijnvoering.time))
# print ("Aantal kritieke trajecten: " + str(besteLijnvoering.kritiekInLijnvoering))

test = LijnVoering('csvFiles/ConnectiesHolland.csv')
test.depthFirstSearch()

# print the runtime
timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))
