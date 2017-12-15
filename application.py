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
import sys

# Own modules and classes
from Algorithms.hillclimberiterator import HillclimberIterator
from Algorithms.greedy import Greedy
from Algorithms.depthfirst import DepthfirstAlgorithm

def main():

    if len(sys.argv) != 5:
        print("Usage: application.py arg1 arg2 arg3 arg4")
        print("Recommended configuration: application.py 500 1600 a True")
        print("arg1: amount of hillclimbers (int > 0, recommended: 500)")
        print("arg2: amount of iterations (int > 0, recommended: 1600)")
        print("arg3: annealing (String[a, b, c, d, e]), recommended: a)")
        print("arg4: show additional details (Bool, recommended: True)")


    else:
        print("filename: " + sys.argv[0])
        print("runs: " + sys.argv[1])
        print("iterations: " + sys.argv[2])
        print("annealing: " + sys.argv[3])
        print("details: " + sys.argv[4])

        # Track how long the application runs
        startTime = datetime.now()

        # Configure the algorithms
        hollandFilepath = 'csvFiles/ConnectiesHolland.csv'
        netherlandsFilepath = 'csvFiles/ConnectiesNationaal.csv'

        # check for positive integer
        try:
            if isinstance(int(sys.argv[1]), int):
                if int(sys.argv[1]) > 0:
                    amountOfHillclimbers = int(sys.argv[1])
                else:
                    print("Please enter a positive integer")
                    return
            else:
                print("Please enter a positive integer")
                return
        except:
            print("Please enter an integer")
            return



        # check for positive integer
        try:
            if isinstance(int(sys.argv[2]), int):
                if int(sys.argv[2]) > 0:
                    iterationsInHillclimber = int(sys.argv[2])
                else:
                    print("Please enter a positive integer")
                    return
            else:
                print("Please enter a positive integer")
                return
        except:
            print("Please enter an integer")
            return


        # check simulated annealing yes/no/cooling strategy/hardcoded
        if sys.argv[3] in ("a", "b", "c", "d", "e"):
            simulatedAnnealing = sys.argv[3]
        else:
            print("use 'a', 'b', 'c', 'd', 'e' for arg3")
            return

        # check for boolean to print details or not
        if sys.argv[4] == "True":
            additionalDetails = True
        elif sys.argv[4] == "False":
            additionalDetails = False
        else:
            print("Use 'True' or 'False' (first letter capitalized) for arg4")
            return

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
        Greedy()


        # Print the runtime
        timeElapsed = datetime.now()-startTime
        print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))

if __name__ == '__main__':
    main()
