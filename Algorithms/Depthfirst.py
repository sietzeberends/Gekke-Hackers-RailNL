from Classes.lijnvoering import Lijnvoering

def DepthfirstAlgorithm(csvFilepath, additionalDetails):
    dfLijnvoering = Lijnvoering(csvFilepath, additionalDetails)
    dfLijnvoering.depthFirstSearch(0, 0, [], {})
