from Classes.trajectory import Trajectory
from Classes.connection import Connection
from Classes.station import Station
from queue import *
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

    def depthFirstSearch(self):
        highScoreLijnvoering = LijnVoering(self.csvFilepath)
        trajectory = Trajectory()
        stack = []
        allTrajectories = []
        time = 0

        # push the first connection on the stack
        stack.append(self.connections[0])
        n = 0
        c = 0

        while len(stack) > 0:
            # count the loop
            n += 1
            print("stacklen :" + str(len(stack)))
            # grab a connection from the stack
            connection = stack.pop()

            # if the time of the connection and the current trajectory combined
            # is too big
            if time + connection.time > 120:
                trajectory.connections.pop()
                time -= connection.time

                for i in range(0,c-1):
                    stack.pop()
                    print("stacklen :" + str(len(stack)))

                connection = stack.pop()

                c = 0
                time -= trajectory.connections[-1].time
                trajectory.connections[-1] = connection
                time += connection.time

            else:
                trajectory.connections.append(connection)
                time += connection.time

            print(trajectory)
            print("time: " + str(time))

            # if/while we haven't reached 120 minutes, append it


            allTrajectories.append(trajectory)
            # edge of civilization check



            if len(connection.children) == 1:
                stack.append(self.connections[child])
            #
            else:
                for child in connection.children:
                    print("")
                    if self.connections[child].station2.name == connection.station1.name:
                        print("bounce, don't add")
                    else:
                        print("add")
                        stack.append(self.connections[child])
                        c += 1

        #
        # # pop the connection, and keep popping while there are still connections left
        #
        #     print (connection)
        #     connection = stack.pop()
        #     time += connection.time
        #     print (connection)
        #     firstTrajectory.connections.append(connection)
        #     if time + connection.time >= 120:
        #         connection = stack.pop()
        #
        #     if connection.station1.name != firstTrajectory.connections[-1].station2.name:
        #
        #         print (time)
        #         print (highScoreLijnvoering)
        #
        #         n = 0
        #         # add the children of the connection
        #         for child in connection.children:
        #             if len(connection.children) == 1:
        #                 stack.append(self.connections[child])
        #             elif n < 1:
        #                 n+= 1
        #             else:
        #                 stack.append(self.connections[child])
        #                 print(stack[-1])
