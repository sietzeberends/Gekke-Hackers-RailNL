from Classes.trajectory import Trajectory
from Classes.connection import Connection

from queue import *
import math
import random

class LijnVoering:
    def __init__(self, connections):
        self.trajectories = []
        self.connections = connections
        self.time = 0
        self.kritiekTotaal = 0


    def __str__(self):
        output = ""
        for trajectory in self.trajectories:
            output += str(trajectory)
            output += "\n\n"
        # output += "Totale tijd van lijnvoering: " + str(self.time)
        return output

    # create a random Lijnvoering
    def createRandomLijnVoering(self, trajectories, amount):

        maxMinutes = 0
        if len(self.connections) <= 56:
            maxMinutes = 120
        else:
            maxMinutes = 180

        # add random trajectories while we haven't created them
        while len(trajectories) < amount:
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections, maxMinutes)
            self.trajectories.append(trajectory)
            self.time += trajectory.time

    def hillClimber(self, trajectories, connections, amount):

        maxMinutes = 0
        if len(self.connections) <= 56:
            maxMinutes = 120
        else:
            maxMinutes = 180

        n = 0
        maxn = 16000
        temperature = 1
        initialTemperature = 1
        self.time = 0

        # create a random Lijnvoering with a certain amount of trajectories
        self.createRandomLijnVoering(self.trajectories, amount)

        # also create a copy of this Lijnvoering in which trajectories
        # can be changed so that we can compare their scores
        alternativeLijnvoering = LijnVoering(connections)

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
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections, maxMinutes)

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

    # queue method (breadth first)
    def queue(self, connections):

        # create the queue
        q = Queue()
        a = {}
        index = 0
        finalList = []

        # put all the root connections in the queue and in the archive as well
        for connection in connections:
            index = str(connection.index)
            connectionList = []
            connectionCheckList = []
            connectionList.append(connection)
            connectionCheckList.append(connection.station1.name)
            q.put(connectionList)
            time = connection.time

        # while there are still items left on the queue
        while q.qsize() > 0:

            # get alkmaar -> hoorn
            connectionFromq = q.get()
            for x in connectionFromq:
                print (x)

            # pak alle children van het laatste item van de lijst (dus alkmaar -> hoorn)
            for child in connectionFromq[-1].children:
                # breid de lijst uit met alle children alkmaar -> hoorn
                # voorkom de bounce
                if connections[child].station2.name not in connectionCheckList:
                    # verander onderstaande naar 120 ipv 180 voor alleen holland
                    if time + connections[child].time <= 180:
                        time += connections[child].time
                        connectionList.append(connections[child])
                        connectionCheckList.append(connections[child].station1.name)
                        q.put(connectionList)
                    else:
                        # als de tijd 120 is, begin met een nieuwe en reset de tijd en sla de connectionlist op
                        finalList.append(connectionList)
                        connectionList.clear()
                        time = 0

        for traject in finalList:
            print("Traject: " + traject[0].station1.name + " -> " + traject[0].station2.name)
            for connection in traject:
                print ("Connectie: " + connection.station1.name + " -> " + connection.station2.name)

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
        self.kritiekTotaal = 0

        for connection in self.connections:
            if connection.critical == True:
                self.kritiekTotaal += 1

        self.kritiekTotaal /= 2

        self.kritiekTotaal = 59
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

        percentageKritiek = (len(indexesAlGecheckt) / 2) / self.kritiekTotaal
        score = percentageKritiek * constanteP - trajecten * constanteTrajecten - minuten / constanteMinuten

        return score
