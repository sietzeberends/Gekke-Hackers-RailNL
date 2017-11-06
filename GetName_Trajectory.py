
class GetName:
    def __init__(self, traject):

        self.connections = traject.connections

        self.Name_traject = []

        for connection in self.connections:
            self.Name_traject.append(connection[0] + " -> ")

    def __str__(self):
        return (self.Name_traject)
