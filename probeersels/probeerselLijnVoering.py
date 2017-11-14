from probeerselTrajectory import Trajectory
from probeerselConnection import Connection

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
    def createRandomLineFeeding(self, trajectories):
        while len(trajectories) < 7:
            trajectory = Trajectory()
            firstConnectionIndex = random.choice(self.connections).index
            trajectory.createTrajectory(firstConnectionIndex, 0 , self.connections)
            self.trajectories.append(trajectory)
            self.time += trajectory.time


    # TODO Alle mogelijke LineFeedings aanmaken
    # Breadth-first
    # def createAllPossibleLineFeedings:

    def LineFeedingScore(self):
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
