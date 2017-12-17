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
    
    b. Run a new hillclimber 500 times. Inside the hillclimber, iterate 1.600 times
  
### Results:

The results don't differ a lot from each other. Also, the temperature doesn't seem to have a lot of influence. The highest score is reached with Geman & Geman's cooling strategy, with a temperature of 750, 500 runs and 1.600.000 iterations:
![alt_text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments//Experiment1CoolingStrategies/SA-500-1600-T750-GEMAN.png)

However, the results when running a new hillclimber 500 times vs. just 5 times do make a difference. Why we think this is happening will be shown in the next experiment.

### Max scores per configuration:

Linear, T750, holland map, 500 runs, 1.600 iterations - 9412

Linear, T1000, holland map, 500 runs, 1.600 iterations - 9406

Linear, T1250, holland map, 500 runs, 1.600 iterations - 9414

Linear, T50000, holland map, 500 runs, 1.600 iterations - 9420


Exponential, T750, holland map, 500 runs, 1.600 iterations - 9514

Exponential, T1000, holland map, 500 runs, 1.600 iterations - 9415

Exponential, T1250, holland map, 500 runs, 1.600 iterations - 9416

Exponential, T50000, holland map, 500 runs, 1.600 iterations - 9418

Geman & Geman, T750, holland map, 500 runs, 1.600 iterations - 9514


Geman & Geman, T1000, holland map, 500 runs, 1.600 iterations - 9410

Geman & Geman, T1250, holland map, 500 runs, 1.600 iterations - 9418

Geman & Geman, T50000, holland map, 500 runs, 1.600 iterations - 9408


Hardcoded, acceptation chance 0.01, holland map, 500 runs, 1.600 iterations - 9411



Linear, T750, holland map, 5 runs, 160.000 iterations - 9389

Linear, T1000, holland map, 5 runs, 160.000 iterations - 9401

Linear, T1250, holland map, 5 runs, 160.000 iterations - 9404

Linear, T50000, holland map, 5 runs, 160.000 iterations - 9399


Exponential, T750, holland map, 5 runs, 160.000 iterations - 9404

Exponential, T1000, holland map, 5 runs, 160.000 iterations - 9401

Exponential, T1250, holland map, 5 runs, 160.000 iterations - 9404

Exponential, T50000, holland map, 5 runs, 160.000 iterations - 9399


Geman & Geman, T750, holland map, 5 runs, 160.000 iterations - 9395

Geman & Geman, T1000, holland map, 5 runs, 160.000 iterations - 9403

Geman & Geman, T1250, holland map, 5 runs, 160.000 iterations - 9409

Geman & Geman, T50000, holland map, 5 runs, 160.000 iterations - 9399


Hardcoded, acceptation chance 0.01, holland map, 5 runs, 160.000 iterations - 9395
