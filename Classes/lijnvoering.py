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
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections)
            self.trajectories.append(trajectory)
            self.time += trajectory.time

    def hillClimber(self, trajectories, connections, amount):

        n = 0
        # create a random Lijnvoering with a certain amount of trajectories
        self.createRandomLijnVoering(self.trajectories, amount)

        # also create a copy of this Lijnvoering in which trajectories
        # can be changed so that we can compare their scores

        alternativeLijnvoering = LijnVoering(connections)
        alternativeLijnvoering.trajectories = self.trajectories

        # set the base score of the Lijnvoering
        score = self.scoreOpdrachtB()

        # track the amount of times we've created a random trajectory
        stopCounter = 0

        # track the time, we can print this out later
        for trajectory in trajectories:
            self.time += trajectory.time

        # start with replacing the first trajectory
        whichTrajectory = 0

        # check for improved score 16.000 times
        while n < 1600000:
            n += 1

            # generate a new random trajectory
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections)

            # replace the trajectory and calculate the new score
            alternativeLijnvoering.trajectories[whichTrajectory] = trajectory
            scoreAlternative = alternativeLijnvoering.scoreOpdrachtB()

            # if the score is better, save this Lijnvoering
            if scoreAlternative > score:
                self.trajectories = alternativeLijnvoering.trajectories
                score = scoreAlternative

                # if there is only one trajectory, replace the same one
                if len(self.trajectories) == 1:
                    whichTrajectory = whichTrajectory

                # if we've reached the last trajectory, start with the first one
                elif len(self.trajectories) - 1 == whichTrajectory:
                    whichTrajectory = 0

                # if we haven't reached the last trajectory, get the next one
                else:
                    whichTrajectory += 1

            # if the score is lower, simulated annealing
            else:
                scores = []
                chanceAlternative = self.acceptationChance(n, score, scoreAlternative) * 100
                round(chanceAlternative,0)
                chanceScore = 100 - chanceAlternative
                scoresAlternative = [scoreAlternative] * int(chanceAlternative)
                scores = [score] * int(chanceScore)
                scores.extend(scoresAlternative)
                score = random.choice(scores)
                stopCounter += 1
                if n % 10000 == 0:
                    print("highscore was: " + str(score))
                    print("alternative score was: " + str(scoreAlternative))
                    print(n)
                    print("acceptatiekans alternatief: " + str(chanceAlternative))
                    # print("verkorting :" str(scoreAlternative - score))
                    # print("temperatuur :" str(10000 * (n/1600000)))

                    print(score)
        return score

    # calculate acception chance for simulated annealing
    def acceptationChance(self, iteration, highscore, alternative):
        # aantal iteraties totaal
        N = 1600000
        verkorting = alternative - highscore
        temperatuur = N - 0.5 * iteration
        # print(temperatuur)
        try:
            chance = math.exp(verkorting/temperatuur)
        except temperatuur == 0:
            verkorting = 0
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
                    if time + connections[child].time <= 120:
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
        constant = 10000
        kritiekTotaal = 20
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
        percentageKritiek = (len(indexesAlGecheckt) / 2) / kritiekTotaal
        score = constant * percentageKritiek
        return score
        # 10000 * aantal kritieke connection in LineFeeding / (aantal kritieke connections totaal)

    def scoreOpdrachtB(self):
        percentageKritiek = 0
        constanteP = 10000
        kritiekTotaal = 20
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

        percentageKritiek = (len(indexesAlGecheckt) / 2) / kritiekTotaal
        score = percentageKritiek * constanteP - trajecten * constanteTrajecten - minuten / constanteMinuten
        return score
