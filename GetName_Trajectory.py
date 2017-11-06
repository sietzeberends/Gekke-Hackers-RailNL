from station import Station
from connection import Connection
from trajectory import Trajectory


class GetName:
    def __init__(self, traject):

        self.Name_traject = []

        for connection in traject.connections:
            self.Name_traject.append(connection.station1 + " -> ")

        last_connection = traject.connections[-1]
        self.Name_traject.append(last_connection.station2)

    def __str__(self):
        return (str(self.Name_traject))
