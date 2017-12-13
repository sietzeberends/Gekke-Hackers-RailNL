from Classes.lijnvoering import Lijnvoering

class HillclimberIterator:
    """Class that creates an amount of Hillclimber that all create a lijnvoering
    The actual Hillclimber is run within the Lijnvoering class
    This class creates new Lijnvoeringen in order to reach different
    starting situations"""

    def __init__(self, mapFilepath, runs, iterations, annealing, details):
        """Args:
            mapFilepath (str)    : a filepath to a csv containing Connections.
            runs        (int)    : the amount of Hillclimbers that are made.
            iterations  (int)    : the amount of iterations each Hillclimber
                                   makes to get a better score.
            annealing   (str)    : indicates whether to use simulated annealing
                                   and which cooling strategy
            details     (boolean): indicates whether additional details are
                                   printed while this algorithm is being runned

            Attributes:
                map (str)            : a filepath to a csv containing Connections.
                runs        (int)    : the amount of Hillclimbers that are made.
                iterations  (int)    : the amount of iterations each Hillclimber
                                       makes to get a better score.
                annealing   (boolean): indicates whether to use simulated annealing
                details     (boolean): indicates whether additional details are
                                       printed while this algorithm is being runned
        """
        self.map = mapFilepath
        self.runs = runs
        self.iterations = iterations
        self.annealing = annealing
        self.details = details

    def algorithm(self):
        """Runs a certain amount of Hillclimbers with or without
        simulated annealing and printing of details.

        Returns: None"""

        highScore = 0
        for i in range(1, self.runs):
            if self.details:
                print("run: " + str(i))

            lijnVoeringHolland = Lijnvoering(self.map, self.details)
            bestLijnvoering = lijnVoeringHolland.hillClimber(self.iterations,
                                                              self.annealing)

            if bestLijnvoering.scoreAssignmentB() > highScore:
            		highScore = bestLijnvoering.scoreAssignmentB()

            if self.details:
                print("Previous highscore: " + str(highScore))
                print("New highscore reached with: " +
                       str(len(bestLijnvoering.trajectories)) + " Trajectories")
                print(bestLijnvoering)
                print ("New highscore: " + str(highScore))
                print ("Total time: " + str(bestLijnvoering.time))
                print ("Amount of critical Connections: " +
                        str(bestLijnvoering.criticalInLijnvoering))
        print("")
        print("Best Lijnvoering has " + str(len(bestLijnvoering.trajectories))
         + " Trajectories and a score of " + str(highScore))
        print("")
        print(str(bestLijnvoering))
        print ("Total time: " + str(bestLijnvoering.time))
        print ("Amount of critical Connections: " +
                str(bestLijnvoering.criticalInLijnvoering))

        lijnvoering = Lijnvoering(self.map, self.details)
        lijnvoering.hillClimber(self.iterations, self.annealing)
