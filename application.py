#!/usr/bin/env python
"""Application file that runs all algorithms for the RailNL case that were
created by Team Gekke Hackers.

Algorithms:

0. Hillclimber > works for Holland map and National map
1. Hillclimber with simulated annealing > works for Holland map and National map
2. Greedy > due to performance only works for Holland map
3. Depthfirst > works for Holland map, but isn't correct and therefore disabled
in this version

__author__ = "Sietze Berends, Daan Uittenhout, Floris Holstege"
__version__ = "1.0"
__maintainer__ = "Sietze Berends"
__email__ = "sietze.berends@student.uva.nl"
__status__ = "Final"
"""

# Built-in modules
from datetime import datetime
import sys

# Own modules and classes
from Algorithms.hillclimberiterator import HillclimberIterator
from Algorithms.greedy import Greedy
from Algorithms.depthfirst import DepthfirstAlgorithm

def main():

    if len(sys.argv) != 6:
        print("Usage: application.py arg1 arg2 arg3 arg4 arg5")
        print("Recommended configuration: application.py 500 1600 a True")
        print("arg1: choose the map (String: 'Holland' or 'National')")
        print("arg2: amount of hillclimbers (int > 0, recommended: 500)")
        print("arg3: amount of iterations (int > 0, recommended: 1600)")
        print("arg4: simulated annealing (String: 'a', 'b', 'c', 'd' or 'e')" +\
              ", recommended: a)")

        print("arg5: show additional details (Bool, recommended: True)")


    else:
        print("filename: " + sys.argv[0])
        print("map: " + sys.argv[1])
        print("runs: " + sys.argv[2])
        print("iterations: " + sys.argv[3])
        print("annealing: " + sys.argv[4])
        print("details: " + sys.argv[5])

        # Track how long the application runs
        startTime = datetime.now()

        # Configure the algorithms
        hollandFilepath = "CsvFiles/ConnectiesHolland.csv"
        netherlandsFilepath = "CsvFiles/ConnectiesNationaal.csv"
        mapChoice = ""
        # check for map
        print(sys.argv[1].lower())
        if (sys.argv[1].lower() != "national" and sys.argv[1].lower() !=
            "holland"):
            print("To choose a map, please enter 'National' or 'Holland'")
            return
        elif sys.argv[1].lower() == "national":
            mapChoice += str(netherlandsFilepath)
        else:
            mapChoice += str(hollandFilepath)

        # check for positive integer
        try:
            if isinstance(int(sys.argv[2]), int):
                if int(sys.argv[2]) > 0:
                    amountOfHillclimbers = int(sys.argv[2])
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
            if isinstance(int(sys.argv[3]), int):
                if int(sys.argv[3]) > 0:
                    iterationsInHillclimber = int(sys.argv[3])
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
        if sys.argv[4] in ("a", "b", "c", "d", "e"):
            simulatedAnnealing = sys.argv[4]
        else:
            print("use 'a', 'b', 'c', 'd', 'e' for arg4")
            return

        # check for boolean to print details or not
        if sys.argv[5].lower() == "true":
            additionalDetails = True
        elif sys.argv[5].lower() == "false":
            additionalDetails = False
        else:
            print("Use 'True' or 'False' for arg5")
            return

        # Run hillclimber algorithm on Holland map
        hc = HillclimberIterator(mapChoice, amountOfHillclimbers
        						 , iterationsInHillclimber, simulatedAnnealing
        						 , additionalDetails)
        hc.algorithm()
        # Run hillclimber algorithm on National map
        hc = HillclimberIterator(mapChoice, amountOfHillclimbers
        				 , iterationsInHillclimber, simulatedAnnealing
        				 , additionalDetails)
        hc.algorithm()

        # Run hillclimber algorithm on Holland map with simulated annealing (linear)
        simulatedAnnealing = "b"
        hcAnnealing = HillclimberIterator(mapChoice, amountOfHillclimbers
        						   , iterationsInHillclimber, simulatedAnnealing
        						   , additionalDetails)
        hcAnnealing.algorithm()

        # Run greedy algorithm on Holland map
        # Greedy()


        # Print the runtime
        timeElapsed = datetime.now()-startTime
        print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))

if __name__ == '__main__':
    main()
