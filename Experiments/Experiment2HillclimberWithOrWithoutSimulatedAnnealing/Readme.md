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
