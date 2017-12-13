#!/usr/bin/env python
"""Application file that runs all algorithms for the RailNL case that were
created by Team Gekke Hackers.

Algorithms:

0. Hillclimber > works for Holland map and National map
1. Hillclimber with simulated annealing > works for Holland map and National map
2. Greedy > due to performance only works for Holland map
3. Depthfirst > works for Holland map, but isn't correct and therefore disabled
in this version

Options:

0: Choose which map to use (use either HollandFilepath or NetherlandsFilepath)
1: Amount of Hillclimbers that are created
2: Amount of iterations that every Hillclimber does.
3: Turn simulated annealing on or off for every Hillclimber
   and Choose a cooling strategy:
   	a: off
	b: linear
	c: exponential
	d: Geman & Geman
	e: hardcoded on a very low acceptation chance

5: Print additional details e.g. new highscores that are reached while
   the algorithm is running"""

__author__ = "Sietze Berends, Daan Uittenhout, Floris Holstege"
__version__ = "1.0"
__maintainer__ = "Sietze Berends"
__email__ = "sietze.berends@student.uva.nl"
__status__ = "Production"

# Built-in modules
from datetime import datetime

# Own modules and classes
from Algorithms.hillclimberiterator import HillclimberIterator

# Track how long the application runs
startTime = datetime.now()

# Configure the algorithms
hollandFilepath = 'csvFiles/ConnectiesHolland.csv'
netherlandsFilepath = 'csvFiles/ConnectiesNationaal.csv'
amountOfHillclimbers = 500
iterationsInHillclimber = 1600
simulatedAnnealing = "a"
additionalDetails = True


# Run hillclimber algorithm on Holland map
hc = HillclimberIterator(hollandFilepath, amountOfHillclimbers
						 , iterationsInHillclimber, simulatedAnnealing
						 , additionalDetails)
hc.algorithm()
# Run hillclimber algorithm on National map
hc = HillclimberIterator(netherlandsFilepath, amountOfHillclimbers
				 , iterationsInHillclimber, simulatedAnnealing
				 , additionalDetails)
hc.algorithm()

# Run hillclimber algorithm on Holland map with simulated annealing (linear)
simulatedAnnealing = "b"
hcAnnealing = HillclimberIterator(hollandFilepath, amountOfHillclimbers
						   , iterationsInHillclimber, simulatedAnnealing
						   , additionalDetails)
hcAnnealing.algorithm()

# Run greedy algorithm on Holland map
from Algorithms.greedy import greedy

greedy.py

# Run depthfirst

# Print the runtime
timeElapsed = datetime.now()-startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))
