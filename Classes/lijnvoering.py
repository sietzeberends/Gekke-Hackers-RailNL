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

            print(str(i) + " trajecten")
            # print("highScore tot nu toe: " + str(self.score))

            n = 0
            maxn = 1600
            temperature = 50000
            initialTemperature = 50000
            self.time = 0

            # create a random Lijnvoering with a certain amount of trajectories
            self.createRandomLijnVoering(self.trajectories, i)

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
                current = alternativeLijnvoering.scoreOpdrachtB()

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

                    temperature = self.newTempExp(initialTemperature, temperature, maxn, n)

                # if the score is lower or equal, simulated annealing
                else:
                      # calculate the chance that the lower score is accepted
                      chanceAlternative = self.acceptationChance(current, scoreAlternative, temperature)
                      chanceRandom = random.choice([0.0, 1.0])

                      # print("cur: " + str(current))
                      # print("alt " + str(scoreAlternative))
                      # print("temp: " + str(temperature))
                      # print("chance: " + str(chanceAlternative))

                      # print("temp: " + str(temperature))
                      # print("verkorting: " + str(scoreAlternative - current))
                      # print("chance: " + str(chanceAlternative))
                      # if it's accepted
                      if chanceAlternative > chanceRandom:
                          current = scoreAlternative
                          self.trajectories.clear()
                          for trajectory in alternativeLijnvoering.trajectories:
                              self.trajectories.append(trajectory)

                      # cool down the temperature for the next run
                      temperature = self.newTempExp(initialTemperature, temperature, maxn, n)

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

                with open ("SA-500-1600-T50000-GEMAN.csv", "a", newline="") as outfile:
                    writer = csv.writer(outfile, dialect="excel")
                    placeholder1 = 		str(len(besteLijnvoering.trajectories)) + ", " +\
                                        str(besteLijnvoering.score) + ", " +\
                                        str(besteLijnvoering.time)
                    placeholder1 = placeholder1.split(",")
                    writer.writerow(placeholder1)

        return besteLijnvoering

    def newTempLinear(self, initialTemperature, temperature, totalIterations, iteration):
        a = iteration/totalIterations
        x = 1
        b = initialTemperature

        temperature = a * -x + b

        return temperature

    def newTempExp(self, initialTemperature, temperature, totalIterations, iteration):
        """Returns the new temperature based on current temperature and
        current iteration"""
        base = (1 / initialTemperature)
        exponent = iteration/totalIterations
        newTemperature = initialTemperature * (base ** exponent)
        return newTemperature

    def newTempGeman(self, initialTemperature, temperature, totalIterations, iteration):
        temperature = initialTemperature / (math.log(iteration + 1))
        return temperature

    def newTempLog(self, initialTemperature, temperature, totalIterations, iteration):
        temperature = Math.log()
        return temperature

    # calculate acception chance for simulated annealing
    def acceptationChance(self, current, alternative, temperature):
        shortening = alternative - current
        chance = math.exp(shortening / temperature)
        return chance

    def depthFirstSearch(self, rootInput, nInput, allTrajectoriesInput, archiveInput):
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
            connection = stack.pop()
            if n == 0 or len(trajectory.connections) == 0:
                trajectory.connections.append(connection)
                trajectory.time += connection.time
                goodToGo = True
                stringKey = ""
                if len(trajectory.connections) > 0:
                    for tconnection in trajectory.connections:
                        stringKey += str(tconnection.index)
                    stringKey += str(connection.index)

            else:
                goodToGo = False
            while not goodToGo:
                print("Trajectory until now: " + str(trajectory))
                print("Try to add : " + str(connection) + " to the trajectory above")
                levelUpIsPossible = False
                willExceedTime = False
                isInArchive = False

                # if we're not good to go, pop the next one
                if len(stack) > 0:
                    print("not good to go, pop the next one")
                    connection = stack.pop()

                # if the stack is empty, go to the next root
                else:
                    print("not good to go, pop the next one")
                    print("nothing left to pop, go to the next root")
                    print (root)
                    if root < 55:
                        root += 1
                        return self.depthFirstSearch(root, n, allTrajectories, archive)
                    else:
                        break

                # check if level up is possible
                # basically, it's possible if the station names match.
                # the connection index however, is not allowed to match
                # we don't want to run the exact same connection twice
                # also, remember how high up we have to go in the tree
                level = 1
                for tconnection in reversed(trajectory.connections):
                    if (connection.station1.name == tconnection.station1.name
                    and connection.index != tconnection.index):
                        levelUpIsPossible = True
                        print("Level up is possible " + str(level) + " levels higher")
                        break
                    else:
                        level += 1

                if not levelUpIsPossible:
                    print("Level up not possible")


                # check if time exceeds
                if trajectory.time + connection.time > 120:
                    willExceedTime = True
                    print("Will exceed time")

                # check if adding the connection to the trajectory
                # would result in a state we already visited
                stringKey = ""
                if len(trajectory.connections) > 0:
                    for tconnection in trajectory.connections:
                        stringKey += str(tconnection.index)
                    stringKey += str(connection.index)

                # and check if it's in the archive
                if stringKey in archive:
                    print("Is in archive")
                    isInArchive = True
                else:
                    print("Is not in archive")
                    isInArchive = False

                # now check if we're good to go
                # if it's not in the archive, we might be good to go
                if not isInArchive:
                    # if it also won't exceed the time: Go!
                    if not willExceedTime:
                        # check if the connection actually matches
                        if connection.station1.name == trajectory.connections[-1].station2.name:
                            print("matches, go.")
                            goodToGo = True
                        else:
                            print("does not match. no go")
                            goodToGo = False
                    else:
                        # if it exceeds the time but we can level up: Go!
                        if levelUpIsPossible:
                            # prepare for appending the connection
                            # which means, pop connections from the trajectory
                            # until we're on the right level in the tree
                            for j in range(0, level):
                                if len(trajectory.connections) > 1:
                                    x = trajectory.connections.pop()
                                    trajectory.time -= x.time
                            print("trajectory after popping: " + str(trajectory))
                            # check if the new trajectory is already in the archive
                            # if so, we're not good to go
                            stringKey = ""
                            if len(trajectory.connections) > 0:
                                for tconnection in trajectory.connections:
                                    stringKey += str(tconnection.index)
                                stringKey += str(connection.index)

                            # and check if it's in the dict
                            if stringKey in archive:
                                print("Is in dict")
                                isInArchive = True
                                goodToGo = False
                            else:
                                print("Is not in dict")
                                isInArchive = False
                                if connection.station1.name == trajectory.connections[-1].station2.name:
                                    print("matches, go.")
                                    goodToGo = True

            # if we're good to go, add the connection to the trajectory
            # and the children to the stack
            if n == 0:
                print("First round, connection already added")
            else:
                trajectory.connections.append(connection)
                trajectory.time += connection.time
                archive[stringKey] = True

            # we append everything, including bounces
            # archive will take care of the rest
            for child in connection.children:
                stack.append(self.connections[child])
                print("child added: " + str(self.connections[child]))

            n += 1
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
                highScore = alternativeScore
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
