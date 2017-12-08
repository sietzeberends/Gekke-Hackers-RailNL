from Classes.trajectory import Trajectory
from Classes.connection import Connection
from Classes.station import Station
from queue import *
import itertools

import math
import random
import csv


class LijnVoering:
    def __init__(self, csvFilepath):
        self.csvFilepath = csvFilepath
        self.trajectories = []
        self.kritiekTotaal = 0
        self.connections = self.loadConnections(csvFilepath)
        self.maxMinutes = self.minutesPerTrajectory(self.connections)
        self.maxTrajectories = self.trajectoriesPerLijnvoering(self.connections)
        self.time = 0
        self.kritiekInLijnvoering = 0
        self.score = 0

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

    def hillClimber(self):

        for i in range(1, self.maxTrajectories):
            highestForThisLijnvoering = 0

            print(str(3) + " trajecten")
            # print("highScore tot nu toe: " + str(self.score))

            n = 0
            maxn = 1600
            temperature = 1
            initialTemperature = 1
            self.time = 0

            # create a random Lijnvoering with a certain amount of trajectories
            self.createRandomLijnVoering(self.trajectories, 3)

            # also create a copy of this Lijnvoering in which trajectories
            # can be changed so that we can compare their scores
            alternativeLijnvoering = LijnVoering(self.csvFilepath)

            for trajectory in self.trajectories:
                alternativeLijnvoering.trajectories.append(trajectory)

            # set the base score of the Lijnvoering
            highestForThisLijnvoering = self.scoreOpdrachtB()

            # track the time, we can print this out later
            for trajectory in self.trajectories:
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
                if scoreAlternative > highestForThisLijnvoering:
                    self.trajectories.clear()
                    for trajectory in alternativeLijnvoering.trajectories:
                        self.trajectories.append(trajectory)

                    highestForThisLijnvoering = scoreAlternative

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

            if highestForThisLijnvoering > self.score:
                besteLijnvoering = LijnVoering(self.csvFilepath)
                for trajectory in self.trajectories:
                    besteLijnvoering.trajectories.append(trajectory)
                    besteLijnvoering.time += trajectory.time
                self.score = highestForThisLijnvoering
                besteLijnvoering.score = self.score
                # print(besteLijnvoering)
                # print ("Nieuwe highscore: " + str(self.score))
                # print ("Totale tijd van lijnvoering: " + str(besteLijnvoering.time))
                # print ("Aantal kritieke trajecten: " + str(besteLijnvoering.kritiekInLijnvoering))

                with open ("csvFiles/connections_visualisation.csv", "w") as outfile:
                    writer = csv.writer(outfile, dialect='excel')
                    for trajectory in besteLijnvoering.trajectories:
                        writer.writerow("-")
                        for connection in trajectory.connections:
                            placeholder = connection.station1.name + ", " +\
                                          connection.station2.name + ", " +\
                                          str(connection.time)
                            placeholder = placeholder.split(",")
                            writer.writerow(placeholder)
                with open ("dataPlot.csv", "a", newline="") as outfile:
                    writer = csv.writer(outfile, dialect="excel")
                    placeholder1 = 		str(len(besteLijnvoering.trajectories)) + ", " +\
                                        str(besteLijnvoering.score) + ", " +\
                                        str(besteLijnvoering.time)
                    placeholder1 = placeholder1.split(",")
                    writer.writerow(placeholder1)

        return besteLijnvoering

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

    def depthFirstSearch(self, rootInput, nInput, allTrajectoriesInput):
        highScoreLijnvoering = LijnVoering(self.csvFilepath)
        trajectory = Trajectory()
        stack = []
        allTrajectories = []
        for traject in allTrajectoriesInput:
            allTrajectories.append(traject)
        exceedsTime = False
        levelUp = False
        inDict = False
        allIsWell = True

        # push the first connection on the stack
        root = rootInput
        stack.append(self.connections[root])
        n = nInput
        dictTrajectory = {}

        while len(stack) > 0:
            # pop a connection from the stack on the first run
            if n == 0:
                connection = stack.pop()
            # if the previous connection was added, pop a new one
            elif allIsWell:
                # print("from stack: " + str(stack[-1]))
                connection = stack.pop()
                # print("to connection: " + str(connection))
            # if the previous connection was not added, we already popped a new one

            # print("Check this connection: " + str(connection))

            # set the stringKey (for checking with the dict)
            stringKey = ""
            if len(trajectory.connections) > 0:
                for tconnection in trajectory.connections:
                    stringKey += str(tconnection.index)
                stringKey += str(connection.index)

            # and check if it's in the dict
            if stringKey in dictTrajectory:
                # print("Is in dict")
                inDict = True
            else:
                # print("Is not in dict")
                inDict = False

            # also check if the connection from the stack belongs to a higher level
            level = 1
            for tconnection in reversed(trajectory.connections):
                if connection.index == tconnection.index:
                    # print("matches " + str(level) + " levels higher")
                    levelUp = True
                    break
                else:
                    level += 1
                    levelUp = False

            if not levelUp:
                levelUp = False

            # finally, check the time
            if trajectory.time + connection.time > 120:
                exceedsTime = True
                # print("Exceeds time")
            else:
                exceedsTime = False
                # print("Does not exceed time")

            # 1. if it's in the dict, pop the next one
            if inDict:
                # print("Already in dict, pop the next one")
                # print("to throw away: " + str(connection))
                connection = stack.pop()
                allIsWell = False

            # 2. if the time is going to exceed 120 minutes, pop the next one
            elif exceedsTime and not levelUp:
                # print("Will exceed time, pop the next one")
                # print("to throw away: " + str(connection))
                connection = stack.pop()
                # print(connection)
                allIsWell = False

            # 3. if the time exceeds but it's from another level, append after going back to that level
            elif exceedsTime and levelUp:
                # print("Will exceed time, but is from higher level. Append to trajectory")
                for j in range(0, level):
                    if len(trajectory.connections) > 1:
                        x = trajectory.connections.pop()
                        trajectory.time -= x.time
                        # print ("new trajectory after deleting " + str(j + 1) + ": " + str(trajectory))

            # 4. if the time doesn't exceed and the connection is from another level but it's not semi-identical to the last one in the trajectory
            elif not exceedsTime and levelUp and connection.station1.name != trajectory.connections[-1].station2.name:
                # print("Will not exceed time, but is from higher level. Append to trajectory")
                for j in range(0, level):
                    if len(trajectory.connections) > 1:
                        x = trajectory.connections.pop()
                        trajectory.time -= x.time
                        # print ("new trajectory after deleting " + str(j + 1) + ": " + str(trajectory))

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
                # print("trajectory for next round: " + str(trajectory))


                # edge of civilization check
                if len(connection.children) == 1:
                    # print(connection)
                    # print(self.connections[self.connections[connection.children[0]].index])
                    # print("edge of civilization, bounce allowed")
                    stack.append(self.connections[self.connections[connection.children[0]].index])


                for tconnection in trajectory.connections:
                    if connection.station2.name == tconnection.station1.name and len(trajectory.connections[0].children) != 1:
                        alreadyExists = True
                        trajectory.connections.pop()
                        break
                    else:
                        alreadyExists = False

                if not alreadyExists:
                    for child in connection.children:
                        # if it's a bounce, don't add it to the stack
                        if connection.station1.name != self.connections[child].station2.name:
                            # print("")
                            # print(self.connections[child])
                            # print("invalid bounce, don't add to stack")
                            # if it's not a bounce, add it to the stack
                        # else:
                            # print(self.connections[child])
                            # print("add to stack: " + str(self.connections[child]))
                            stack.append(self.connections[child])

                if root == 24:
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


        # else:
        #     bestLijnvoering = LijnVoering(self.csvFilepath)
        #     bestTrajectory = Trajectory()
        #     bestLijnvoering.trajectories.append(bestTrajectory)
        #     alternativeLijnvoering = LijnVoering(self.csvFilepath)
        #     alternativeTrajectory = Trajectory()
        #     alternativeLijnvoering.trajectories.append(alternativeTrajectory)
        #
        #     highScore = 0
        #     for at in allTrajectories:
        #         print(at)
        #         alternativeLijnvoering.trajectories[0] = at
        #         alternativeScore = alternativeLijnvoering.scoreOpdrachtB()
        #         print(alternativeScore)
        #         if alternativeScore > highScore:
        #             bestLijnvoering.trajectories[0] = at
        #             highScore = bestLijnvoering.scoreOpdrachtB()
        #     print("The best Lijnvoering: ")
        #     print(bestLijnvoering)
        #     print(highScore)
        #     print("Amount of critical connections: " + str(bestLijnvoering.kritiekInLijnvoering))
        #     print (len(allTrajectories))
        #     print(n)

        self.combineDepthFirst(allTrajectories)

    def combineDepthFirst(self, trajectories):
        n = 0
        lijnVoering = LijnVoering('csvFiles/ConnectiesHolland.csv')
        alternativeLijnVoering = LijnVoering('csvFiles/ConnectiesHolland.csv')
        highScore = 0
        for combination in itertools.product(trajectories, trajectories, trajectories):
            alternativeLijnVoering.trajectories.clear()
            n += 1
            if n % 1000000 == 0:
                print(n)
            for trajectory in combination:
                alternativeLijnVoering.trajectories.append(trajectory)
            alternativeScore = alternativeLijnVoering.scoreOpdrachtB()
            if alternativeScore > highScore:
                lijnVoering.trajectories.clear()
                for trajectory in alternativeLijnVoering.trajectories:
                    lijnVoering.trajectories.append(trajectory)
                highScore = lijnVoering.scoreOpdrachtB()
        print(lijnVoering)
        print(lijnVoering.scoreOpdrachtB())

    def ScoreOpdrachtA(self):
        for connection in connections:
            if connection.critical == "TRUE":
                self.kritiekTotaal += 1
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
        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.kritiekTotaal
        score = constant * percentageKritiek
        return score
        # 10000 * aantal kritieke connection in LineFeeding / (aantal kritieke connections totaal)

    def scoreOpdrachtB(self):
        self.kritiekInLijnvoering = 0
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
                            self.kritiekInLijnvoering += 1
                        # als de connectie op een oneven positie staat, voeg de connectie toe (en z'n broertje ook)
                        else:
                            indexesAlGecheckt.append(connection.index)
                            indexesAlGecheckt.append(self.connections[connection.index + 1].index)
                            self.kritiekInLijnvoering += 1


        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.kritiekTotaal
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
                self.kritiekTotaal += 1

        # divide, because you can go hence and forth
        self.kritiekTotaal /= 2

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
