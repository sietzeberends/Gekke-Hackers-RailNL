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
    def createAllPossibleLijnVoeringen(self, connections, indexVerticaal, indexHorizontaal, tree):

        # als we voor het eerst de functie doorlopen
        if indexVerticaal == 0 and indexHorizontaal == 0:
            v = indexVerticaal
            h = indexHorizontaal

            tree = {}

            # maak dan de tree aan met alle connecties
            for connection in connections:
                tree[v, h] = connection.index
                h += 1

            # for key, value in tree.items():
            #     print(key, value)

        # als het niet de eerste keer is, neem dan de oude tree over
        else:
            tree = tree

        indexVerticaal += 1
        allChilds = connections[indexHorizontaal].children
        childsRemaining = len(allChilds)
        for child in allChilds:
            if connections[child].station2.name == connections[indexHorizontaal].station1.name:
                # als de volgende connectie  maar 1 child heeft (Dordrecht/Den Helder)
                if len(connections[child].children) == 1:
                    tree[indexVerticaal, indexHorizontaal] = child
                    indexHorizontaal += 1
                    print(indexHorizontaal)
                    childsRemaining -= 1
                # als de herkomst hetzelfde is als de bestemming
                else:
                    childsRemaining -= 1

            # alles klopt
            else:
                tree[indexVerticaal, indexHorizontaal] = child
                childsRemaining -= 1
                indexHorizontaal += 1
                print(indexHorizontaal)

        print (child)
        # als het laatste child van de connectie geweest is, begin dan aan de children van de volgende connectie
        if childsRemaining == 0:
            if len(connections[child].children) == 1:
                indexHorizontaal += 1
            return self.createAllPossibleLijnVoeringen(connections, indexVerticaal, indexHorizontaal, tree)

        # als de children van de laatste connectie geweest zijn, begin dan aan de children van het eerste child van de eerste connectie
        if indexVerticaal == len(connections):
            indexVerticaal += 1
            indexHorizontaal = 0
            # childConnecties = []
            # for connection in connections:
            #     for childIndex in allChilds:
            #         if childIndex == connection.indexes:
            #             childConnecties.append(connection)
            return self.createAllPossibleLijnVoeringen(childConnecties, index, tree)

        return "asd"

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
