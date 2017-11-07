for connection in connections
x = random.choice(connections)
  if connection.station2 == x.station1 && connection.time < 120 - x.time:
    trajectory.append(connections)

def addconnection()
    connectionsForFirstTrajectory.expend(random.choice(connections))
    while trajectory.time < 120:
        x = random.choice(connections)
        if x.station2 == connectionsForFirstTrajectory[-1].station1:
          connectionsForFirstTrajectory.append(x)
