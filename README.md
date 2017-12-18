# RailNL

Group: Team Gekke Hackers
Members: Sietze Berends, Floris Holstege & Daan Uittenhout

Case: RailNL - finding an optimal Lijnvoering for a fictional railway company. For more information: http://heuristieken.nl/wiki/index.php?title=RailNL

## Getting started

### Prerequisites
1. Powershell/Cmd
2. Python 3.6.3

### Running the program
The application is run by executing application.py with command line arguments:

      application.py arg1 arg2 arg3 arg4 arg5

The following arguments should be given:

arg1: Choose which map to use:

      National
      Holland

arg2: Amount of Hillclimbers that are created:

      Positive integer 

arg3: Amount of iterations that every Hillclimber does -> change the value of iterationsInHillclimber:

      Positive integer

arg4: Turn simulated annealing on or off for every Hillclimber and choose a cooling strategy:

      a: off
      b: linear
      c: exponential
      d: Geman & Geman
      e: hardcoded on a very low acceptation chance
  
arg5: print additional details e.g. new highscores that are reached while the algorithm is running:

      True
      False

## Structure
0. The application is run by executing application.py from the main folder
1. All classes are kept in a seperate 'Classes' folder
2. Algorithms are kept in an 'Algorithm' folder
3. Files necessary for experiments are kept in an 'Experiments' 

## Experiments:
The following experiments have been done:

0 - Manipulating the score function
1 - Different simulated annealing cooling strategies and temperatures
2 - Hillclimber with or without simulated annealing
3 - Disable Utrecht
4 - All stations critical

All experiments are placed in a folder called Experiments and have their own subfolder with a Readme. Please refer to these Experiments to get the description, results and plots of each experiments.

## Visualisation:

Our visualisation depicts the final solutions that we have found. The following link will bring you to our index page, where you then will be taken to our visualisation. 

https://sietzeberends.github.io/Gekke-Hackers-RailNL/
