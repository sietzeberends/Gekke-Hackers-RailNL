from Classes.trajectory import Trajectory
from Classes.connection import Connection

from queue import *
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
        output += "Totale tijd van lijnvoering: " + str(self.time)
        return output

    # Willekeurige LineFeeding aanmaken, dit kunnen we al.
    def createRandomLijnVoering(self, trajectories, amount):
        # rand = random.randrange(8)
        # print(rand)
        while len(trajectories) < amount:
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections)
            self.trajectories.append(trajectory)
            self.time += trajectory.time

    def hillClimber(self, trajectories, connections, amount):
        self.createRandomLijnVoering(self.trajectories, amount)
        alternativeLijnvoering = LijnVoering(connections)
        alternativeLijnvoering.trajectories = self.trajectories
        score = self.scoreOpdrachtB()
        stopCounter = 0
        for trajectory in trajectories:
            self.time += trajectory.time

        # start with replacing the first trajectory
        whichTrajectory = 0

        while stopCounter < 16000:
            # print(score)
            # generate a new trajectory
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections)

            # replace the trajectory and calculate the new score
            alternativeLijnvoering.trajectories[whichTrajectory] = trajectory
            scoreAlternative = alternativeLijnvoering.scoreOpdrachtB()

            # if the score is better, get the next trajectory
            if scoreAlternative > score:
                self.trajectories = alternativeLijnvoering.trajectories
                score = scoreAlternative

                # move on to the next trajectory
                # go to the first trajectory after the last one

                # if there is only one trajectory, replace the same one
                if len(self.trajectories) == 1:
                    whichTrajectory = whichTrajectory

                # if we've reached the last trajectory, start with the first one
                elif len(self.trajectories) - 1 == whichTrajectory:
                    whichTrajectory = 0

                # if we haven't reached the last trajectory, get the next one
                else:
                    whichTrajectory += 1

            else:
                stopCounter += 1

        # print(stopCounter)
        # print(len(self.trajectories))
        # for traject in self.trajectories:
        #     print("\n")
        #     for connection in traject.connections:
        #         print(connection)

        return score


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
