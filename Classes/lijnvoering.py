from Classes.trajectory import Trajectory
from Classes.connection import Connection
from Classes.station import Station

import itertools
import math
import random
import csv


class Lijnvoering:
    """Class that contains a Lijnvoering and all algorithms."""

    def __init__(self, csvFilepath, details):
        """Args:
            csvFilepath (str): a filepath to a CSV containing Connections
            details (boolean): indicates whether additional details are printed
                               while this algorithm is being runned.

           Attributes:
            csvFilepath (str)          : a filepath to a CSV containing
                                         Connections
            trajectories (list)        : list with all Trajectories in this
                                         Lijnvoering
            criticalTotal (int)        : the maximum amount of critical
                                         Connections that is possible
            connections (list)         : all possible Connections
            maxMinutes (int)           : the maximum amount of minutes that is
                                         allowed per Trajectory
            maxTrajectories (int)      : the maximum amount of Trajectories that
                                         is allowed per Lijnvoering
            time (int)                 : the sum of the time of all Connections
                                         in this Lijnvoering
            criticalInLijnvoering (int): the amount of critical Connections in
                                         this Lijnvoering
            score(int)                 : the score of this Lijnvoering
            details(boolean)           : indicates whether additional details
                                         are printed while algorithms are being
                                         runned
            """
        self.csvFilepath = csvFilepath
        self.trajectories = []
        self.criticalTotal = 0
        self.connections = self.loadConnections(csvFilepath)
        self.maxMinutes = self.minutesPerTrajectory(self.connections)
        self.maxTrajectories = self.trajectoriesPerLijnvoering(self.connections)
        self.time = 0
        self.criticalInLijnvoering = 0
        self.score = 0
        self.details = details

    def __str__(self):
        output = ""
        i = 1
        for trajectory in self.trajectories:
            output += "trajectory " + str(i) + ": " + str(trajectory) + "\n\n"
            i += 1
        return output

    def createRandomLijnvoering(self, amount):
        """Creates a random Lijnvoering

           Args:
            amount (int): the amount of Trajectories to add to the Lijnvoering

           Returns: None
        """

        # add random trajectories while we haven't created them
        while len(self.trajectories) < amount:
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0,
                                        self.connections, self.maxMinutes)
            self.trajectories.append(trajectory)
            self.time += trajectory.time

    def hillClimber(self, iterations, annealing):
        """Runs the hillclimber algorithm on a random Lijnvoering

           Args:
            iterations (int): the maximum amount of iterationsthat the
                              hillClimber is to get a better score with
                              replacing one Trajectory. After this, the
                              hillClimber goes to the next Trajectory
            annealing (str) : determines whether simulated annealing is used in
                              the algorithm and if so, which cooling strategy is
                              used

           Returns: Lijnvoering
        """

        if annealing == "a":
            simulatedAnnealing = False
            str
        elif annealing == "b":
            simulatedAnnealing = True
            strategy = getattr(self, "newTempLinear")
        elif annealing == "c":
            simulatedAnnealing = True
            strategy = getattr(self, "newTempExp")
        elif annealing == "d":
            simulatedAnnealing = True
            strategy = getattr(self, "newTempGeman")
        elif annealing == "e":
            simulatedAnnealing = True

        for i in range(1, self.maxTrajectories):
            highestForThisLijnvoering = 0

            if self.details:
                print(str(i) + " trajectories")

            n = 0
            maxN = iterations
            temperature = 50000
            initialTemperature = 50000
            self.time = 0

            # create a random Lijnvoering with a certain amount of trajectories
            self.createRandomLijnvoering(i)

            # also create a copy of this Lijnvoering in which trajectories
            # can be changed so that we can compare their scores
            alternativeLijnvoering = Lijnvoering(self.csvFilepath, self.details)

            for trajectory in self.trajectories:
                alternativeLijnvoering.trajectories.append(trajectory)

            # set the base score of the Lijnvoering
            highestForThisLijnvoering = self.scoreAssignmentB()

            # track the time, we can print this out later
            for trajectory in self.trajectories:
                self.time += trajectory.time

            # start with replacing the first Trajectory
            whichTrajectory = 0

            # check for improved score maxN times
            while n < maxN:
                n += 1

                # generate a new random Trajectory
                trajectory = Trajectory()
                firstConnectionIndex = random.choice(self.connections).index
                trajectory.createTrajectory(firstConnectionIndex, 0,
                                            self.connections, self.maxMinutes)

                # replace the trajectory and calculate the new score
                alternativeLijnvoering.trajectories[whichTrajectory] = (
                trajectory)
                scoreAlternative = alternativeLijnvoering.scoreAssignmentB()
                current = alternativeLijnvoering.scoreAssignmentB()

                # if the score is better, save this Lijnvoering
                if scoreAlternative > highestForThisLijnvoering:
                    self.trajectories.clear()
                    for trajectory in alternativeLijnvoering.trajectories:
                        self.trajectories.append(trajectory)

                    highestForThisLijnvoering = scoreAlternative

                    # if there is only one trajectory, replace the same one
                    if len(self.trajectories) == 1:
                        whichTrajectory = whichTrajectory

                    # if the last trajectory is reached start with the first one
                    elif len(self.trajectories) - 1 == whichTrajectory:
                        whichTrajectory = 0

                    # if we haven't reached the last trajectory get the next one
                    else:
                        whichTrajectory += 1

                    # set the new temperature
                    if simulatedAnnealing:
                        temperature = strategy(initialTemperature, temperature,
                                               maxN, n)

                # if the score is lower or equal, simulated annealing
                else:
                    if simulatedAnnealing:
                        # calculate the chance that the lower score is accepted
                          if annealing == "e":
                              chanceAlternative == 0.01
                          else:
                              chanceAlternative = self.acceptationChance(current
                                                , scoreAlternative, temperature)
                              chanceRandom = random.choice([0.00, 1.00])

                          # replace trajectory with alternative if accepted
                          if chanceAlternative > chanceRandom:
                              current = scoreAlternative
                              self.trajectories.clear()
                              for trajectory in (
                              alternativeLijnvoering.trajectories):
                                  self.trajectories.append(trajectory)

                          # cool down the temperature for the next run
                          temperature = strategy(initialTemperature,
                                                 temperature, maxN, n)

            # if the score is higher, replace the Lijnvoering and write the csv
            if highestForThisLijnvoering > self.score:
                besteLijnvoering = Lijnvoering(self.csvFilepath, self.details)
                for trajectory in self.trajectories:
                    besteLijnvoering.trajectories.append(trajectory)
                    besteLijnvoering.time += trajectory.time
                self.score = highestForThisLijnvoering
                besteLijnvoering.score = self.score

                # with open ("csvFiles/connections_visualisation.csv",
                #            "w") as out:
                #     writer = csv.writer(out, dialect='excel')
                #     for trajectory in besteLijnvoering.trajectories:
                #         writer.writerow("-")
                #         for connection in trajectory.connections:
                #             placeholder = connection.station1.name + ", " +\
                #                           connection.station2.name + ", " +\
                #                           str(connection.time)
                #             placeholder = placeholder.split(",")
                #             writer.writerow(placeholder)
                # # filename depends on parameters
                # filename = ""
                # if simulatedAnnealing:
                #     filename += "SA-" + "500-" + str(maxN) + "-T"
                #     filename += str(initialTemperature) + "-"
                #     if strategy == "b":
                #         filename += "LIN.csv"
                #     elif strategy == "c":
                #         filename += "EXP.csv"
                #     elif strategy == "d":
                #         filename += "GEMAN.csv"
                #     else:
                #         filename += "HARDCODED"
                # else:
                #     filename += "HC-" + "500-" + str(maxN) + ".csv"
                #
                # with open (filename, "a", newline="") as out:
                #     writer = csv.writer(out, dialect="excel")
                #     placeholder1 =	str(len(besteLijnvoering.trajectories)) +\
                #                     ", " + str(besteLijnvoering.score) + ", " +\
                #                     str(besteLijnvoering.time)
                #     placeholder1 = placeholder1.split(",")
                #     writer.writerow(placeholder1)

        return besteLijnvoering

    def newTempLinear(self, initialTemperature, temperature, totalIterations,
                      iteration):
        """Calculates the new temperature with a linear cooling strategy.

           Args:
           initialTemperature (int): the initialTemperature that the Hillclimber
                                     starts with
           temperature (int)       : the current temperature
           totalIterations (int)   : the total amount of iterations that the
                                     Hillclimber does
           iteration (int)         : the current iteration

           Returns: the new temperature (int)
        """

        a = iteration/totalIterations
        x = 1
        b = initialTemperature

        temperature = a * -x + b
        return temperature

    def newTempExp(self, initialTemperature, temperature, totalIterations,
                   iteration):
        """Calculates the new temperature with an exponential cooling strategy.

           Args:
           initialTemperature (int): the initialTemperature that the Hillclimber
                                     starts with
           temperature (int)       : the current temperature
           totalIterations (int)   : the total amount of iterations that the
                                     Hillclimber does
           iteration (int)         : the current iteration

           Returns: the new temperature (int)
        """

        base = (1 / initialTemperature)
        exponent = iteration/totalIterations
        newTemperature = initialTemperature * (base ** exponent)
        return newTemperature

    def newTempGeman(self, initialTemperature, temperature, totalIterations,
                     iteration):
        """Calculates the new temperature with Geman & Geman's cooling strategy.

           Args:
           initialTemperature (int): the initialTemperature that the Hillclimber
                                     starts with
           temperature (int)       : the current temperature
           totalIterations (int)   : the total amount of iterations that the
                                     Hillclimber does
           iteration (int)         : the current iteration

           Returns: the new temperature (int)
        """

        temperature = initialTemperature / (math.log(iteration + 1))
        return temperature

    # calculate acception chance for simulated annealing
    def acceptationChance(self, current, alternative, temperature):
        """Calculates the acceptation chance.

           Args:
            current (long): the current highscore
            alternative(long): the proposed

           Returns: the acceptation chance (float)
        """

        shortening = alternative - current
        chance = math.exp(shortening / temperature)
        return chance

    def depthFirstSearch(self):

        stack = []
        archive = {}
        trajectory = Trajectory()
        besteLijnvoering = Lijnvoering(self.csvFilepath, self.details)
        n = 0
        nogFfDoor = 10000000000
        root = 0
        allTrajectories = []

        # loop over alle connecties
        for rConnection in self.connections:
            trajectory.connections.clear()
            trajectory.time = 0
            print (root)
            root += 1
            if root > 1:
                if stringKey == "23-49-45-46-42":
                    nogFfDoor = n
            if nogFfDoor == 224300:
                break

            # voeg de root connectie toe aan de stack
            stack.append(rConnection)
            print("Root connection: " + str(rConnection))

            # pop a connection off the stack
            while len(stack) > 0:

                goodToGo = False
                timeIsOkay = False
                notInArchive = False
                connection = stack.pop()
                if root > 1:
                    if stringKey == "23-49-45-46-42":
                        nogFfDoor = n
                if nogFfDoor == 224300:
                    break

                if len(trajectory.connections) > 0:
                    print("current trajectory: " + str(trajectory))
                    print("connection to check: " + str(connection))

                # check alle condities
                while not goodToGo:
                    print("NNNNNNNN: " + str(n))
                    if n > 0:
                        # if the stations don't connect, pop from the trajectory
                        while (len(trajectory.connections) > 0 and
                               connection.index not in
                               trajectory.connections[-1].children):
                            trajectory.time -= trajectory.connections[-1].time
                            trajectory.connections.pop()
                            print("doesn't connect, trajectory after popping: "
                                  + str(trajectory))

                    stringKey = ""
                    if len(trajectory.connections) > 0:
                        for tconnection in trajectory.connections:
                            stringKey += str(tconnection.index) + '-'

                    stringKey += str(connection.index)
                    print("stringkey: " + stringKey)
                    if stringKey == "23-49-45-46-42":
                        nogFfDoor = n
                    if nogFfDoor == 224300:
                        break

                    # if in archive
                    if stringKey in archive:
                        print("In archive")
                        break

                    else:
                        print("Not in archive")
                        notInArchive = True

                    print("check time")

                    # if exceeds time
                    if trajectory.time + connection.time > 120:
                        print("exceeds time")
                        break
                    else:
                        print("doesn't exceed time")
                        timeIsOkay = True

                    if notInArchive and timeIsOkay:
                        print("good to go")
                        goodToGo = True
                    else:
                        print("not good to go")

                # if good to go, add to trajectory
                if goodToGo:
                    trajectory.connections.append(connection)
                    trajectory.time += connection.time
                    toAppend = Trajectory()
                    for tConnection in trajectory.connections:
                        toAppend.connections.append(tConnection)
                        toAppend.time += tConnection.time
                    allTrajectories.append(toAppend)

                    # add trajectory to archive
                    archive[stringKey] = True

                    # add children for the connection
                    for child in connection.children:
                        print("append child " + str(self.connections[child]))
                        stack.append(self.connections[child])

                n += 1
                nogFfDoor += 1

        highScore = 0
        m = 0
        # for aTrajectory in allTrajectories:
        #     print (m)
        #     m += 1
        #     alternativeLijnvoering = Lijnvoering(self.csvFilepath, self.details)
        #     trajectToAdd = Trajectory()
        #     for aConnection in aTrajectory.connections:
        #         trajectToAdd.connections.append(aConnection)
        #         trajectToAdd.time += aConnection.time
        #     alternativeLijnvoering.trajectories.append(trajectToAdd)
        #     alternativeScore = alternativeLijnvoering.scoreAssignmentB()
        #
        #     if alternativeScore > highScore:
        #         besteLijnvoering.trajectories.clear()
        #         besteLijnvoering.trajectories.append(trajectToAdd)
        #         highScore = alternativeScore
        #
        # with open ("filename1", "a", newline="") as out:
        #     writer = csv.writer(out, dialect="excel")
        #
        #     for connection in besteLijnvoering.trajectories[0].connections:
        #         placeholder1 =	str(connection) + ", "
        #         writer.writerow(placeholder1)
        #
        #     placeholder1 = str(highScore)
        #     writer.writerow(placeholder1)

    def combineDepthFirst(self, trajectories):
        n = 0
        lijnVoering = Lijnvoering('csvFiles/ConnectiesHolland.csv')
        alternativeLijnvoering = Lijnvoering('csvFiles/ConnectiesHolland.csv')
        highScore = 0
        for combination in itertools.product(trajectories, trajectories,
                                             trajectories):
            alternativeLijnvoering.trajectories.clear()
            n += 1
            if n % 1000000 == 0:
                print(n)
            for trajectory in combination:
                alternativeLijnvoering.trajectories.append(trajectory)
            alternativeScore = alternativeLijnvoering.scoreAssignmentB()
            if alternativeScore > highScore:
                lijnVoering.trajectories.clear()
                for trajectory in alternativeLijnvoering.trajectories:
                    lijnVoering.trajectories.append(trajectory)
                highScore = alternativeScore
        print(lijnVoering)
        print(lijnVoering.scoreAssignmentB())


    def ScoreAssignmentA(self):
        """Calculates the score for assignment A

           Returns: the score (float)
        """

        for connection in connections:
            if connection.critical == "TRUE":
                self.criticalTotal += 1
        constant = 10000
        indexesAlGecheckt = []
        percentageKritiek = 0
        for trajectory in self.trajectories:
            for connection in trajectory.connections:
                if connection.critical:
                    if connection.index not in indexesAlGecheckt:
                        if connection.index % 2 != 0:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections
                                                [connection.index - 1].index)
                        else:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections
                                                [connection.index + 1].index)
        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.criticalTotal
        score = constant * percentageKritiek
        return score

    def scoreAssignmentB(self):
        """Calculates the score for assignment B

           Returns: the score (float)
        """

        self.criticalInLijnvoering = 0
        percentageKritiek = 0
        constanteP = 10000

        trajecten = 0
        constanteTrajecten = 50
        minuten = 0
        constanteMinuten = 1
        indexesAlGecheckt = []

        for trajectory in self.trajectories:
            minuten += trajectory.time
            trajecten += 1

            for connection in trajectory.connections:

                if connection.critical:

                    if connection.index not in indexesAlGecheckt:

                        if connection.index % 2 != 0:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(connection.index - 1)
                            self.criticalInLijnvoering += 1

                        else:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(connection.index + 1)
                            self.criticalInLijnvoering += 1

        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.criticalTotal
        score = ((percentageKritiek * constanteP) -
                (trajecten * constanteTrajecten) - (minuten / constanteMinuten))

        return score

    def loadConnections(self, connectionsFilepath):
        """Loads all connections based on a CSV

           Args:
            connectionsFilepath (str): a filepath to a CSV containing
                                       Connections

           Returns: all connections (list)
        """

        # connections second
        connectionsList = []
        index = 0;
        with open(connectionsFilepath, 'r') as csvfile:
            rows = csv.reader(csvfile)

            for row in rows:
                connectionsList.append(Connection(Station(row[0], "", "",
                                       row[3]), Station(row[1], "", "", row[3]),
    							       row[2], row[3], index))
                index += 1

                connectionsList.append(Connection(Station(row[1], "", "",
                                       row[3]), Station(row[0], "", "", row[3]),
    								   row[2], row[3], index))
                index += 1

    	# add the children to the connections
        # count how many connection are critical
        for connection in connectionsList:
            connection.addChildren(connectionsList)
            if connection.critical == True:
                self.criticalTotal += 1

        # divide, because you can go hence and forth
        self.criticalTotal /= 2

        return connectionsList

    def minutesPerTrajectory(self, connections):
    	"""Calculates the allowed amount of minutes per trajectory

           Args:
            connections (list) : list with all Connections

           Returns: the amount of minutes that is allowed per trajectory (int)
        """
    	minutes = 0
    	if len(connections) <= 56:
    		minutes = 120
    	else:
    		minutes = 180

    	return minutes

    def trajectoriesPerLijnvoering(self, connections):
        """Calculates the allowed amount of trajectories

           Args:
            connections (list) : list with all Connections

           Returns: the amount of trajectories that is allowed per Lijnvoering
                    (int)
        """
        trajectories = 0
        if len(connections) <= 56:
            trajectories = 8
        else:
            trajectories = 21

        return trajectories

    def loadConnectionsAndStations(self, connectionsFilepath, stationsFilepath):
        """Load stations and connections from CSV files

           Args:
            connectionsFilepath (String) : path to a CSV with all Connections
            stationsFilepath (String)    : path to a CSV with all Stations

           Returns: the list with all connections (list)
        """

        # first the stations
        stationsList = []
        with open(stationsFilepath, 'r') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                stationsList.append(Station(row[0], row[1], row[2], row[3]))

        # now the connections
        connectionsList = []
        index = 0;
        with open(connectionsFilepath, 'r') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                connectionsList.append(Connection(Station(row[0], "", "",
                                       row[3]), Station(row[1], "", "", row[3]),
                                       row[2], row[3], index))
                index += 1

                connectionsList.append(Connection(Station(row[1], "", "",
                                       row[3]), Station(row[0], "", "", row[3]),
                                       row[2], row[3], index))
                index += 1

        # add the children to the connections
        for connection in connectionsList:
            connection.addChildren(connectionsList)

        return connectionsList
