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

## Experiment 0 - manipulating the score function:
For calculating the score of our Lijnvoering, we've used both the original scorefunction as well as our own, alternated function. We changed the penalty for having an extra trajectory or minute in order to let these variables have a lot more impact on our final result. 

### The original score function:

S = p*10000 - (t*20 + min/100000)

### Our score function:

S = p*10000 - (t*50 + min)

### Results:
Best score with original score function on national map: 9779.98214:
![alt text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/HC-OriginalScore-500-1600-NAT.png)

Best score with our own score function on national map: 7673.016949:
![alt_text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/HC-500-1600%20-%20NAT.png)

Our score function resulted in lower scores. We expect that the best results of both score functions will also have different amounts of trajectories and use different connections due to a different impact of these variables.

## Experiment 1 - different simulated annealing cooling strategies and temperatures:
In the program we've applied several cooling strategies for the simulated annealing. We also used several values for the initial- and end temperatures. Combinations with the following parameters have been tried:

1. Cooling strategy:

  a. Linear
  
  b. Exponential
  
  c. Geman & Geman
  
  d. No cooling strategy, instead, us a hardcoded acceptation chance of 0.01 in order to compare results with the regular hillclimber
  
2. Temperature:

  a. T = 750
  
  b. T = 1.000
  
  c. T = 1.250
  
  d. T = 50.000
  
3. Map:

  a. Map with connections in the provinces of North- and South Holland
  
  b. Map with connection from The Netherlands
  

4. Runs/Iterations:

  a. Run a new hillclimber 5 times. Inside the hillclimber, iterate 1.600.000 times
  
  b. Run a new hillclimber 500 times. Inside the hillclimber, iterate 16.000 times
  
### Results:

The results don't differ a lot from each other. Also, the temperature doesn't seem to have a lot of influence. The highest score is reached with Geman & Geman's cooling strategy, with a temperature of 750, 500 runs and 1.600.000 iterations:
![alt_text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/SA-500-1600-T750-GEMAN.png)

However, the results when running a new hillclimber 500 times vs. just 5 times do make a difference. Why we think this is happening will be shown in the next experiment.

### Max scores per configuration:

Linear, T750, holland map, 500 runs, 16.000 iterations - 9412

Linear, T1000, holland map, 500 runs, 16.000 iterations - 9406

Linear, T1250, holland map, 500 runs, 16.000 iterations - 9414

Linear, T50000, holland map, 500 runs, 16.000 iterations - 9420


Exponential, T750, holland map, 500 runs, 16.000 iterations - 9514

Exponential, T1000, holland map, 500 runs, 16.000 iterations - 9415

Exponential, T1250, holland map, 500 runs, 16.000 iterations - 9416

Exponential, T50000, holland map, 500 runs, 16.000 iterations - 9418

Geman & Geman, T750, holland map, 500 runs, 16.000 iterations - 9514


Geman & Geman, T1000, holland map, 500 runs, 16.000 iterations - 9410

Geman & Geman, T1250, holland map, 500 runs, 16.000 iterations - 9418

Geman & Geman, T50000, holland map, 500 runs, 16.000 iterations - 9408


Hardcoded, acceptation chance 0.01, holland map, 500 runs, 16.000 iterations - 9411



Linear, T750, holland map, 5 runs, 1.600.000 iterations - 9389

Linear, T1000, holland map, 5 runs, 1.600.000 iterations - 9401

Linear, T1250, holland map, 5 runs, 1.600.000 iterations - 9404

Linear, T50000, holland map, 5 runs, 1.600.000 iterations - 9399


Exponential, T750, holland map, 5 runs, 1.600.000 iterations - 9404

Exponential, T1000, holland map, 5 runs, 1.600.000 iterations - 9401

Exponential, T1250, holland map, 5 runs, 1.600.000 iterations - 9404

Exponential, T50000, holland map, 5 runs, 1.600.000 iterations - 9399


Geman & Geman, T750, holland map, 5 runs, 1.600.000 iterations - 9395

Geman & Geman, T1000, holland map, 5 runs, 1.600.000 iterations - 9403

Geman & Geman, T1250, holland map, 5 runs, 1.600.000 iterations - 9409

Geman & Geman, T50000, holland map, 5 runs, 1.600.000 iterations - 9399


Hardcoded, acceptation chance 0.01, holland map, 5 runs, 1.600.000 iterations - 9395

## Experiment 2 - simulated annealing vs. hillclimber:
In the program we've run several cooling strategies for the simulated annealing, but we also ran hillclimbers that don't use simulated annealing. All the simulated annealing strategies from experiment 1 have been compared with the following hillclimbers:

Hillclimber, 500 runs, 16.000 iteration

Hillclimber, 5 runs, 1.600.000 iterations

### Results:
When looking at the results of the hillclimber and the simulated annealing, the hillclimber performs better. While this is strange at first sight, we think there might be a logical explanation for this: when making an iteration, our hillcimber replaces a whole trajectory at once, which means that pretty large 'steps' are taken. Therefore, it doesn't profit from simulated annealing. 

Best hillclimber without simulated annealing for Holland map:

![alt_text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/HC-500-1600.png)

Best hillclimber without simulated annealing for National map:

![alt_text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/HC-500-1600-NAT.png)

### Max scores per configuration:

Hillclimber, 500 runs, 16.000 iteration - 9405

Hillclimber, 5 runs, 1.600.000 iterations - 9515


## Experiment 3 - disable Utrecht:
Utrecht is a very important station in The Netherlands and has a lot of critical connections around it. To measure the importance of this station we ran the maps of Holland with both Utrecht and without Utrecht to see the difference.

### Results:
The results are still being processed at the moment and will be available in the final version of this project.

## Experiment 4 - make all stations critical:
Making all connections critical should have quite an impact on the score, given the score function that we are using (not the original one). This can be done on both the national map and the holland map.

### Results:
The scores when all connections are critical drop when compared with the plots of Experiment 2.

Best score on Holland map when all connections are critical:
![alt_text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/HC-Critical-500-1600.png)

Best score on National map when all connections are critical:
![alt_text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/HC-Critical-500-1600-NAT.png)

