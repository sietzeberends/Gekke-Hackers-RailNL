
class GetName:
    def __init__(self, connection):

        self.station1 = connection.station1
        self.station2 = connection.station2

    def __str__(self):
        
        return (self.station1 + " -> " + self.station2)
