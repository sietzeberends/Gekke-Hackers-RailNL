<<<<<<< current
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
            csvFilepath (str)          : a filepath to a CSV containing Connections
            trajectories (list)        : list with all Trajectories in this Lijnvoering
            criticalTotal (int)        : the maximum amount of critical Connections that
                                         is possible
            connections (list)         : all possible Connections
            maxMinutes (int)           : the maximum amount of minutes that is allowed
                                         per Trajectory
            maxTrajectories (int)      : the maximum amount of Trajectories that is
                                         allowed per Lijnvoering
            time (int)                 : the sum of the time of all Connections in
                                         this Lijnvoering
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

    def createRandomLijnVoering(self, amount):
        """Creates a random Lijnvoering

           Args:
            amount (int): the amount of Trajectories to add to the Lijnvoering

           Returns: None"""

        # add random trajectories while we haven't created them
        while len(self.trajectories) < amount:
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections, self.maxMinutes)
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

           Returns: Lijnvoering"""

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
            self.createRandomLijnVoering(i)

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

                with open ("csvFiles/connections_visualisation.csv",
                           "w") as out:
                    writer = csv.writer(out, dialect='excel')
                    for trajectory in besteLijnvoering.trajectories:
                        writer.writerow("-")
                        for connection in trajectory.connections:
                            placeholder = connection.station1.name + ", " +\
                                          connection.station2.name + ", " +\
                                          str(connection.time)
                            placeholder = placeholder.split(",")
                            writer.writerow(placeholder)
                # filename depends on parameters
                filename = ""
                if simulatedAnnealing:
                    filename += "SA-" + "500-" + str(maxN) + "-T"
                    filename += str(initialTemperature) + "-"
                    if strategy == "b":
                        filename += "LIN.csv"
                    elif strategy == "c":
                        filename += "EXP.csv"
                    elif strategy == "d":
                        filename += "GEMAN.csv"
                    else:
                        filename += "HARDCODED"
                else:
                    filename += "HC-" + "500-" + str(maxN) + ".csv"

                with open (filename, "a", newline="") as out:
                    writer = csv.writer(out, dialect="excel")
                    placeholder1 =	str(len(besteLijnvoering.trajectories)) +\
                                    ", " + str(besteLijnvoering.score) + ", " +\
                                    str(besteLijnvoering.time)
                    placeholder1 = placeholder1.split(",")
                    writer.writerow(placeholder1)

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

           Returns: the new temperature"""

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

           Returns: the new temperature"""

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

           Returns: the new temperature"""

        temperature = initialTemperature / (math.log(iteration + 1))
        return temperature

    # calculate acception chance for simulated annealing
    def acceptationChance(self, current, alternative, temperature):
        """Calculates the acceptation chance.

           Args:
            current (long): the current highscore
            alternative(long): the proposed

           Returns: the acceptation chance"""

        shortening = alternative - current
        chance = math.exp(shortening / temperature)
        return chance

    def depthFirstSearch(self, rootInput, nInput, allTrajectoriesInput,
                         archiveInput):
        """"""
        highScoreLijnvoering = LijnVoering(self.csvFilepath)
        trajectory = Trajectory()
        stack = []
        allTrajectories = []
        for traject in allTrajectoriesInput:
            allTrajectories.append(traject)
        allIsWell = True

        # push the first connection on the stack
        root = rootInput
        stack.append(self.connections[root])
        n = nInput
        archive = archiveInput

        while len(stack) > 0:
            # pop a connection from the stack on the first run
            if n == 0:
                connection = stack.pop()
            # if the previous connection was added, pop a new one
            elif allIsWell:
                print("from stack: " + str(stack[-1]))
                connection = stack.pop()
                print("to connection: " + str(connection))
            # if the previous connection was not added
            # we already popped a new one
            else:
                print("Keep going...")

            print("Check this connection: " + str(connection))

            # set the stringKey (for checking with the dict)
            stringKey = ""
            if len(trajectory.connections) > 0:
                for tconnection in trajectory.connections:
                    stringKey += str(tconnection.index)
                stringKey += str(connection.index)

            # and check if it's in the dict
            if stringKey in dictTrajectory:
                print("Is in dict")
                inDict = True
            else:
                print("Is not in dict")
                inDict = False

            # also check if the connection from the stack
            # belongs to a higher level
            level = 1
            for tconnection in reversed(trajectory.connections):
                if connection.station1.name == tconnection.station1.name:
                    print("matches " + str(level) + " levels higher")
                    levelUp = True
                    break
                else:
                    level += 1
                    levelUp = False

            if not levelUp:
                print("Not from a higher level")

            # finally, check the time
            if trajectory.time + connection.time > 120:
                exceedsTime = True
                print("Exceeds time")
            else:
                exceedsTime = False
                print("Does not exceed time")

            # 1. if it's in the dict, pop the next one
            if inDict:
                print("Already in dict, pop the next one")
                print("to throw away: " + str(connection))
                connection = stack.pop()
                allIsWell = False

            # 2. if the time is going to exceed 120 minutes, pop the next one
            elif exceedsTime and not levelUp:
                print("Will exceed time, pop the next one")
                print("to throw away: " + str(connection))
                for connection in stack:
                    print("STACK PRINTEN")
                    print(connection)
                connection = stack.pop()
                print(connection)
                allIsWell = False

            # 3. if the time exceeds but it's from another level,
            # append after going back to that level
            elif exceedsTime and levelUp:
                print("Will exceed time, but is from higher level. +\
                       Append to trajectory")
                for j in range(0, level):
                    if len(trajectory.connections) > 1:
                        x = trajectory.connections.pop()
                        trajectory.time -= x.time
                        print ("new trajectory after deleting " + str(j + 1) +\
                               ": " + str(trajectory))

            # 4. if the time doesn't exceed and the connection is from another
            # level but it's not identical to the last one in the trajectory
            elif not (exceedsTime and levelUp and
        connection.station1.name != trajectory.connections[-1].station2.name):
                print("Will not exceed time, but is from higher level. +\
                      Append to trajectory")
                for j in range(0, level):
                    if len(trajectory.connections) > 1:
                        x = trajectory.connections.pop()
                        trajectory.time -= x.time
                        print ("new trajectory after deleting " + str(j + 1) +\
                               ": " + str(trajectory))

            # 5. if all is well, add children (not level up version)
            else:
                trajectory.connections.append(connection)
                trajectory.time += connection.time
                shadowTrajectory = Trajectory()
                for c in trajectory.connections:
                    shadowTrajectory.connections.append(c)
                    shadowTrajectory.time += c.time
                allTrajectories.append(shadowTrajectory)
                dictTrajectory[stringKey] = True
                print("trajectory for next round: " + str(trajectory))


                # edge of civilization check
                if len(connection.children) == 1:
                    print(connection)
                    print(self.connections[self.connections[connection.children[0]].index])
                    print("edge of civilization, bounce allowed")
                    stack.append(self.connections[self.connections[connection.children[0]].index])


                for tconnection in trajectory.connections:
                    if (connection.station2.name == tconnection.station1.name
                        and len(trajectory.connections[0].children) != 1):
                        alreadyExists = True
                        trajectory.connections.pop()
                        break
                    else:
                        alreadyExists = False

                if not alreadyExists:
                    for child in connection.children:
                        # if it's a bounce, don't add it to the stack
                        if (connection.station1.name ==
                            self.connections[child].station2.name):
                            print("")
                            print(self.connections[child])
                            print("invalid bounce, don't add to stack")
                            # if it's not a bounce, add it to the stack
                        else:
                            print(self.connections[child])
                            print("add to stack: " +\
                                   str(self.connections[child]))
                            stack.append(self.connections[child])

                if root == 55:
                    break

                allIsWell = True

            n += 1


        if len(stack) == 0:
            level = 1
            for tconnection in reversed(trajectory.connections):
                if connection.station1.name == tconnection.station1.name:
                    break
                else:
                    level += 1

            for j in range(0, level):
                if len(trajectory.connections) > 1:
                    x = trajectory.connections.pop()
                    trajectory.time -= x.time
            if connection.time + trajectory.time <= 120:
                trajectory.connections.append(connection)
                trajectory.time += connection.time

            shadowTrajectory = Trajectory()
            for c in trajectory.connections:
                shadowTrajectory.connections.append(c)
                shadowTrajectory.time += c.time
            allTrajectories.append(shadowTrajectory)

        root += 1

        if root < 56:
            return self.depthFirstSearch(root, n, allTrajectories)


        else:
            bestLijnvoering = LijnVoering(self.csvFilepath)
            bestTrajectory = Trajectory()
            bestLijnvoering.trajectories.append(bestTrajectory)
            alternativeLijnvoering = LijnVoering(self.csvFilepath)
            alternativeTrajectory = Trajectory()
            alternativeLijnvoering.trajectories.append(alternativeTrajectory)

            highScore = 0
            for at in allTrajectories:
                print(at)
                alternativeLijnvoering.trajectories[0] = at
                alternativeScore = alternativeLijnvoering.scoreAssignmentB()
                print(alternativeScore)
                if alternativeScore > highScore:
                    bestLijnvoering.trajectories[0] = at
                    highScore = bestLijnvoering.scoreAssignmentB()
            print("The best Lijnvoering: ")
            print(bestLijnvoering)
            print(highScore)
            print("Amount of critical connections: " +\
                  str(bestLijnvoering.criticalInLijnvoering))
            print (len(allTrajectories))
            print(n)

        self.combineDepthFirst(allTrajectories)

    def combineDepthFirst(self, trajectories):
        n = 0
        lijnVoering = LijnVoering('csvFiles/ConnectiesHolland.csv')
        alternativeLijnVoering = LijnVoering('csvFiles/ConnectiesHolland.csv')
        highScore = 0
        for combination in itertools.product(trajectories, trajectories,
                                             trajectories):
            alternativeLijnVoering.trajectories.clear()
            n += 1
            if n % 1000000 == 0:
                print(n)
            for trajectory in combination:
                alternativeLijnVoering.trajectories.append(trajectory)
            alternativeScore = alternativeLijnVoering.scoreAssignmentB()
            if alternativeScore > highScore:
                lijnVoering.trajectories.clear()
                for trajectory in alternativeLijnVoering.trajectories:
                    lijnVoering.trajectories.append(trajectory)
                highScore = alternativeScore
        print(lijnVoering)
        print(lijnVoering.scoreAssignmentB())


    def ScoreAssignmentA(self):
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
                            indexesAlGecheckt.append(self.connections[connection.index - 1].index)
                        else:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections[connection.index + 1].index)
        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.criticalTotal
        score = constant * percentageKritiek
        return score

    def scoreAssignmentB(self):
        self.criticalInLijnvoering = 0
        percentageKritiek = 0
        constanteP = 10000

        trajecten = 0
        constanteTrajecten = 50
        minuten = 0
        constanteMinuten = 1
        indexesAlGecheckt = []

        # ga alle trajecten in de lijnvoering langs
        for trajectory in self.trajectories:
            minuten += trajectory.time
            trajecten += 1
            # en alle connecties per traject
            for connection in trajectory.connections:
                # kijk of de connectie kritiek is
                if connection.critical:
                    # als de connectie al eerder is meegerekend
                    if connection.index not in indexesAlGecheckt:
                        # als de connectie op een oneven positie staat, voeg de connectie toe (en z'n broertje ook)
                        if connection.index % 2 != 0:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections[connection.index - 1].index)
                            self.criticalInLijnvoering += 1
                        # als de connectie op een oneven positie staat, voeg de connectie toe (en z'n broertje ook)
                        else:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections[connection.index + 1].index)
                            self.criticalInLijnvoering += 1


        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.criticalTotal
        score = percentageKritiek * constanteP - trajecten * constanteTrajecten - minuten / constanteMinuten

        return score

    def loadConnections(self, connectionsFilepath):
        """Loads all connections based on a CSV and returns them as a list"""
        # connections second
        connectionsList = []
        index = 0;
        with open(connectionsFilepath, 'r') as csvfile:
            rows = csv.reader(csvfile)

            for row in rows:
                connectionsList.append(Connection(Station(row[0], "", "", row[3]),
    										  Station(row[1], "", "", row[3]),
    										  row[2], row[3], index))

                index += 1

                connectionsList.append(Connection(Station(row[1], "", "", row[3]),
    										  Station(row[0], "", "", row[3]),
    										  row[2],
    										  row[3], index))

                index += 1

    	# add the children to the connections and count how many connections are critical
        for connection in connectionsList:
            connection.addChildren(connectionsList)
            if connection.critical == True:
                self.criticalTotal += 1

        # divide, because you can go hence and forth
        self.criticalTotal /= 2

        return connectionsList

    def minutesPerTrajectory(self, connections):
    	"""Calculates the allowed amount of minutes per trajectory and returns that number"""
    	minutes = 0
    	if len(connections) <= 56:
    		minutes = 120
    	else:
    		minutes = 180

    	return minutes

    def trajectoriesPerLijnvoering(self, connections):
        """Calculates the allowed amount of trajectories and returns that number"""
        trajectories = 0
        if len(connections) <= 56:
            trajectories = 8
        else:
            trajectories = 21

        return trajectories
=======
from Classes.trajectory import Trajectory
from Classes.connection import Connection
from Classes.station import Station

from queue import *
import math
import random
import csv

class LijnVoering:
    def __init__(self, connectionsFilepath, stationsFilepath):
        self.connectionsFilepath = connectionsFilepath
        self.stationsFilepath = stationsFilepath
        self.connections = self.loadConnectionsAndStations(self.connectionsFilepath,
                                                           self.stationsFilepath)

        self.criticalTotal = 0
        self.maxTrajectories = 0
        self.maxMinutes = 0

        self.setVariables(self.connections)

        self.trajectories = []
        self.time = 0

    def __str__(self):
        output = ""
        for trajectory in self.trajectories:
            output += str(trajectory)
            output += "\n\n"
        # output += "Totale tijd van lijnvoering: " + str(self.time)
        return output

    # create a random Lijnvoering
    def createRandomLijnVoering(self, trajectories, amount):

        # add random trajectories while we haven't created them
        while len(trajectories) < amount:
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections, self.maxMinutes)
            self.trajectories.append(trajectory)
            self.time += trajectory.time

    def hillClimber(self, trajectories, connections, amount, runs):

        n = 0
        maxn = 16000
        temperature = 1
        initialTemperature = 1
        self.time = 0

        # create a random Lijnvoering with a certain amount of trajectories
        self.createRandomLijnVoering(self.trajectories, amount)

        # also create a copy of this Lijnvoering in which trajectories
        # can be changed so that we can compare their scores
        alternativeLijnvoering = LijnVoering(self.connectionsFilepath, self.stationsFilepath)

        for trajectory in self.trajectories:
            alternativeLijnvoering.trajectories.append(trajectory)

        # set the base score of the Lijnvoering
        current = self.scoreOpdrachtB()

        # track the time, we can print this out later
        for trajectory in trajectories:
            self.time += trajectory.time

        # start with replacing the first trajectory
        whichTrajectory = 0

        # check for improved score 16.000 times
        while n < maxn:
            n += 1

            # generate a new random trajectory
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections, self.maxMinutes)

            # replace the trajectory and calculate the new score
            alternativeLijnvoering.trajectories[whichTrajectory] = trajectory
            scoreAlternative = alternativeLijnvoering.scoreOpdrachtB()

            # if the score is better, save this Lijnvoering
            if scoreAlternative > current:
                self.trajectories.clear()
                for trajectory in alternativeLijnvoering.trajectories:
                    self.trajectories.append(trajectory)

                current = scoreAlternative

                # if there is only one trajectory, replace the same one
                if len(self.trajectories) == 1:
                    whichTrajectory = whichTrajectory

                # if we've reached the last trajectory, start with the first one
                elif len(self.trajectories) - 1 == whichTrajectory:
                    whichTrajectory = 0

                # if we haven't reached the last trajectory, get the next one
                else:
                    whichTrajectory += 1

                temperature = self.newTemp(initialTemperature, temperature, maxn, n)

            # if the score is lower or equal, simulated annealing
            # else:
            #       # calculate the chance that the lower score is accepted
            #       chanceAlternative = self.acceptationChance(current, scoreAlternative, temperature)
            #       chanceRandom = random.choice([0.0, 1.0])
            #
            #       # print("cur: " + str(current))
            #       # print("alt " + str(scoreAlternative))
            #       # print("temp: " + str(temperature))
            #       # print("chance: " + str(chanceAlternative))
            #
            #       # print("temp: " + str(temperature))
            #       # print("verkorting: " + str(scoreAlternative - current))
            #       # print("chance: " + str(chanceAlternative))
            #       # if it's accepted
            #       if chanceAlternative > chanceRandom:
            #           current = scoreAlternative
            #           self.trajectories.clear()
            #           for trajectory in alternativeLijnvoering.trajectories:
            #               self.trajectories.append(trajectory)
            #
            #       # cool down the temperature for the next run
            #       temperature = self.newTemp(initialTemperature, temperature, maxn, n)


            return current

    def newTemp(self, initialTemperature, temperature, totalIterations, iteration):
        """Returns the new temperature based on current temperature and
        current iteration"""
        base = (1 / initialTemperature)
        exponent = iteration/totalIterations
        newTemperature = initialTemperature * (base ** exponent)
        return newTemperature

    # calculate acception chance for simulated annealing
    def acceptationChance(self, current, alternative, temperature):
        shortening = alternative - current
        chance = math.exp(shortening / temperature)
        return chance

    def ScoreOpdrachtA(self):
        constant = 10000
        indexesAlGecheckt = []
        percentageKritiek = 0
        for trajectory in self.trajectories:
            for connection in trajectory.connections:
                if connection.critical:
                    if connection.index not in indexesAlGecheckt:
                        if connection.index % 2 != 0:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections[connection.index - 1].index)
                        else:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections[connection.index + 1].index)
        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.criticalTotal
        score = constant * percentageKritiek
        return score
        # 10000 * aantal kritieke connection in LineFeeding / (aantal kritieke connections totaal)

    def scoreOpdrachtB(self):

        percentageKritiek = 0
        constanteP = 10000

        trajecten = 0
        constanteTrajecten = 50
        minuten = 0
        constanteMinuten = 1
        indexesAlGecheckt = []

        # ga alle trajecten in de lijnvoering langs
        for trajectory in self.trajectories:
            minuten += trajectory.time
            trajecten += 1
            # en alle connecties per traject
            for connection in trajectory.connections:
                # kijk of de connectie kritiek is
                if connection.critical:
                    # als de connectie al eerder is meegerekend
                    if connection.index not in indexesAlGecheckt:
                        # als de connectie op een oneven positie staat, voeg de connectie toe (en z'n broertje ook)
                        if connection.index % 2 != 0:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections[connection.index - 1].index)
                        # als de connectie op een oneven positie staat, voeg de connectie toe (en z'n broertje ook)
                        else:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections[connection.index + 1].index)

        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.criticalTotal
        score = percentageKritiek * constanteP - trajecten * constanteTrajecten - minuten / constanteMinuten

        return score

    def loadConnectionsAndStations(self, connectionsFilepath, stationsFilepath):
        """Load stations and connections from CSV files and returns them as a list"""

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
                connectionsList.append(Connection(Station(row[0], "", "", row[3]),
                Station(row[1], "", "", row[3]), row[2], row[3], index))

                index += 1

                connectionsList.append(Connection(Station(row[1], "", "", row[3]),
                Station(row[0], "", "", row[3]), row[2], row[3], index))

                index += 1

        # add the children to the connections
        for connection in connectionsList:
            connection.addChildren(connectionsList)

        return connectionsList

    def setVariables(self, connections):
        """Calculates the amount of critical connections
        The maximum amount of trajectories that are allowed
        And the maximum amount of minutes that is allowed per Trajectory"""

        for connection in self.connections:
            if connection.critical == True:
                self.criticalTotal += 1
        # divided by two, because you can go back and forth
        self.criticalTotal /= 2

        if len(connections) <= 56:
            # actually 7, but we use range(1,8)
            self.maxTrajectories = 8
            self.maxMinutes = 120
        else:
            # actually 20, but we use range(1,21)
            self.maxTrajectories = 21
            self.maxMinutes = 180
>>>>>>> before discard
