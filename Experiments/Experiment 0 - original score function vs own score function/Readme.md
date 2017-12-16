## Experiment 0 - manipulating the score function:
For calculating the score of our Lijnvoering, we've used both the original scorefunction as well as our own, alternated function. We changed the penalty for having an extra trajectory or minute in order to let these variables have a lot more impact on our final result. 

### The original score function:

S = p*10000 - (t*20 + min/100000)

### Our score function:

S = p*10000 - (t*50 + min)

### Results:
Best score with original score function on national map: 9779.98214:
![alt text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/Experiment 0 - original score function vs own score function/HC-OriginalScore-500-1600-NAT.png)

Best score with our own score function on national map: 7673.016949:
![alt_text](https://github.com/sietzeberends/Gekke-Hackers-RailNL/blob/master/Experiments/Experiment 0 - original score function vs own score function/HC-500-1600%20-%20NAT.png)

Our score function resulted in lower scores. We expect that the best results of both score functions will also have different amounts of trajectories and use different connections due to a different impact of these variables.
