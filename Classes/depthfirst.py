def depthFirstSearch(self):
    highScoreLijnvoering = LijnVoering(self.csvFilepath)
    trajectory = Trajectory()
    stack = []
    allTrajectories = []

    time = 0

    # push the first connection on the stack
    root = 0
    stack.append(self.connections[root])
    n = 0
    dictTrajectories = {}


    while len(stack) > 0:
        # count the loops
        n += 1
        # grab a connection from the stack
        connection = stack.pop()
        print("connection in treatment:")
        print(connection)

        if len(trajectory.connections) == 0:
            trajectory.connections.append(connection)

        # if the time would exceed 120 minutes
        while time + connection.time > 120:
            print("time would exceed 120 minutes, get next one: ")
            connection = stack.pop()
            print(connection)

            level = 1
            for tconnection in reversed(trajectory.connections):
                if connection.station1.name == tconnection.station1.name:
                    print("matches " + str(level) + " levels higher")
                    for j in range(0, level):
                        if len(trajectory.connections) > 1:
                            x = trajectory.connections.pop()
                            time -= x.time
                            print ("new trajectory after deleting " + str(j) + ": " + str(trajectory))
                    break
                else:
                    level += 1

        print("append if not in dict")
        stringKey = ""
        for tconnection in trajectory.connections:
            stringKey += str(tconnection.index)
        stringKey += str(connection.index)
        print("stringKey: " + stringKey)

        # als die in de dict zit, pop de volgende
        if stringKey in dictTrajectories:
            print("already in dict! pop next one")
        else:
            print("not yet in dict! add it")
            trajectory.connections.append(connection)
            time += connection.time
            allTrajectories.append(trajectory)
            dictTrajectories[stringKey] = True

        print (trajectory)
        print (time)

        # edge of civilization check
        if len(connection.children) == 1:
            print(connection)
            print(self.connections[self.connections[connection.children[0]].index])
            print("edge of civilization, bounce allowed")
            stack.append(self.connections[self.connections[connection.children[0]].index])

        # if the connection has multiple children
        else:
            for child in connection.children:
                # if it's a bounce, don't add it to the stack
                if connection.station1.name == self.connections[child].station2.name:
                    print(self.connections[child])
                    print("invalid bounce, don't add to stack")
                # if it's not a bounce, add it to the stack
                else:
                    print(self.connections[child])
                    print("add to stack")
                    stack.append(self.connections[child])

        if len(stack) == 0:
            root += 1
            stack.append(self.connections[root])

        if n > 1100:
            print("blabla")
            break
