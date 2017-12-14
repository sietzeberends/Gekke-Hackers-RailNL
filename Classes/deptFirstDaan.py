def depthFirstSearch(self, rootInput, nInput, allTrajectoriesInput):
      highScoreLijnvoering = LijnVoering(self.csvFilepath)
      trajectory = Trajectory()
      stack = []
      allTrajectories = []
      for traject in allTrajectoriesInput:
          allTrajectories.append(traject)
      exceedsTime = False
      levelUp = False
      inDict = False
      allIsWell = True

      # push the first connection on the stack
      root = rootInput
      stack.append(self.connections[root])
      n = nInput
      dictTrajectory = {}

      while len(stack) > 0:


          # pop a connection from the stack on the first run
          if n == 0:
              connection = stack.pop()
          # if the previous connection was added, pop a new one
          elif allIsWell:
              print("from stack: " + str(stack[-1]))
              connection = stack.pop()
              print("to connection: " + str(connection))
          # if the previous connection was not added, we already popped a new one
          else:
              print("Keep going...")

          print("Check this connection: " + str(connection))

          # set the stringKey (for checking with the dict)
          stringKey = ""
          if len(trajectory.connections) > 0:
              for tconnection in trajectory.connections:
                  stringKey += str(tconnection.index)
              stringKey += str(connection.index)

          # and check if it's in the dict
          if stringKey in dictTrajectory:
              print("Is in dict")
              inDict = True
          else:
              print("Is not in dict")
              inDict = False

          # also check if the connection from the stack belongs to a higher level
          level = 1
          for tconnection in reversed(trajectory.connections):
              if connection.station1.name == tconnection.station1.name:
                  print("matches " + str(level) + " levels higher")
                  levelUp = True
                  break
              else:
                  level += 1
                  levelUp = False

          if not levelUp:
              print("Not from a higher level")

          # finally, check the time
          if trajectory.time + connection.time > 120:
              exceedsTime = True
              print("Exceeds time")
          else:
              exceedsTime = False
              print("Does not exceed time")

          # 1. if it's in the dict, pop the next one
          if inDict:
              print("Already in dict, pop the next one")
              print("to throw away: " + str(connection))
              connection = stack.pop()
              allIsWell = False

          # 2. if the time is going to exceed 120 minutes, pop the next one
          elif exceedsTime and not levelUp:
              print("Will exceed time, pop the next one")
              print("to throw away: " + str(connection))
              for connection in stack:
                  print("STACK PRINTEN")
                  print(connection)
              connection = stack.pop()
              print(connection)
              allIsWell = False

          # 3. if the time exceeds but it's from another level, append after going back to that level
          elif exceedsTime and levelUp:
              print("Will exceed time, but is from higher level. Append to trajectory")
              for j in range(0, level):
                  if len(trajectory.connections) > 1:
                      x = trajectory.connections.pop()
                      trajectory.time -= x.time
                      print ("new trajectory after deleting " + str(j + 1) + ": " + str(trajectory))

          # 4. if the time doesn't exceed and the connection is from another level but it's not semi-identical to the last one in the trajectory
          elif not exceedsTime and levelUp and connection.station1.name != trajectory.connections[-1].station2.name:
              print("Will not exceed time, but is from higher level. Append to trajectory")
              for j in range(0, level):
                  if len(trajectory.connections) > 1:
                      x = trajectory.connections.pop()
                      trajectory.time -= x.time
                      print ("new trajectory after deleting " + str(j + 1) + ": " + str(trajectory))

          # 5. if all is well, add children (not level up version)
          else:
              if len(trajectory.connections) > 0:
                  while trajectory.connections[-1].station1 == connection.station2.name:
                      connection = stack.pop()
              trajectory.connections.append(connection)
              trajectory.time += connection.time
              shadowTrajectory = Trajectory()
              for c in trajectory.connections:
                  shadowTrajectory.connections.append(c)
                  shadowTrajectory.time += c.time
              allTrajectories.append(shadowTrajectory)
              dictTrajectory[stringKey] = True
              print("trajectory for next round: " + str(trajectory))


              # edge of civilization check
              if len(connection.children) == 1:
                  print(connection)
                  print(self.connections[self.connections[connection.children[0]].index])
                  print("edge of civilization, bounce allowed")
                  stack.append(self.connections[self.connections[connection.children[0]].index])
                  break

              for tconnection in trajectory.connections:

                  if connection.station2.name == tconnection.station1.name and len(trajectory.connections[0].children) != 1:
                      if connection.index == tconnection.index:
                          alreadyExists = True
                          x = trajectory.connections.pop()
                          break
                      else:
                          for child in connection.children:
                              if child != tconnection.index and self.connections[child].station2.name != connection.station1.name:
                                  stack.append(self.connections[child])
                          break
                  else:
                      alreadyExists = False


              if not alreadyExists:
                  for child in connection.children:
                      # if it's a bounce, don't add it to the stack
                      if connection.station1.name == self.connections[child].station2.name:
                          print("")
                          print(self.connections[child])
                          print("invalid bounce, don't add to stack")
                          # if it's not a bounce, add it to the stack
                      else:
                          print(self.connections[child])
                          print("add to stack: " + str(self.connections[child]))
                          stack.append(self.connections[child])


              allIsWell = True
              n += 1


      if len(stack) == 0:
          level = 1
          for tconnection in reversed(trajectory.connections):
              if connection.station1.name == tconnection.station1.name:
                  break
              else:
                  level += 1

          for j in range(0, level):
              if len(trajectory.connections) > 1:
                  x = trajectory.connections.pop()
                  trajectory.time -= x.time
          if connection.time + trajectory.time <= 120:
              trajectory.connections.append(connection)
              trajectory.time += connection.time

          shadowTrajectory = Trajectory()
          for c in trajectory.connections:
              shadowTrajectory.connections.append(c)
              shadowTrajectory.time += c.time
          allTrajectories.append(shadowTrajectory)

      root += 1

      if root < 56:
          return self.depthFirstSearch(root, n, allTrajectories)


      else:
          bestLijnvoering = LijnVoering(self.csvFilepath)
          bestTrajectory = Trajectory()
          bestLijnvoering.trajectories.append(bestTrajectory)
          alternativeLijnvoering = LijnVoering(self.csvFilepath)
          alternativeTrajectory = Trajectory()
          alternativeLijnvoering.trajectories.append(alternativeTrajectory)

          highScore = 0
          for at in allTrajectories:
              print(at)
              alternativeLijnvoering.trajectories[0] = at
              alternativeScore = alternativeLijnvoering.scoreOpdrachtB()
              print(alternativeScore)
              if alternativeScore > highScore:
                  bestLijnvoering.trajectories[0] = at
                  highScore = bestLijnvoering.scoreOpdrachtB()
          print("The best Lijnvoering: ")
          print(bestLijnvoering)
          print(highScore)
          print("Amount of critical connections: " + str(bestLijnvoering.kritiekInLijnvoering))
          print (len(allTrajectories))
          print(n)