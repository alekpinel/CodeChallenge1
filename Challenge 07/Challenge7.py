# coding=utf-8
'''
  14/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 7 - Escape or Die
'''

# Directions:
# 0 - North
# 1 - West
# 2 - South
# 3 - East

import random

directions = ['north', 'west', 'south', 'east']
directionsByName = {0:'north', 1:'west', 2:'south', 3:'east'}

class Dungeon():
    def __init__(self):
        self.STOP_COMMAND = 'STOP'
        self.REANUDE_COMMAND = 'REANUDE'
        self.IS_EXIT_COMMAND = 'is exit?'
        
        self.manual = False
        
        self.map = Map()
        self.map.loadMap()
        
        self.lastMovement = -1
        self.attemptedPosition = (0, 0)
        
        self.plan = None
    

    def mainLoop(self, data):
        if ('Welcome, my friend! You are at the beginning of a long dark dungeon.' in data):
            return self.decideNextMove()
        elif ('Ouch. It seems you can\'t go there' in data):
            return self.blockedInput()
        elif ('Great movement. Here is your new position:' in data):
            return self.correctInput()
        elif ('No. Sorry, traveller...' in data):
            return self.noExit()
        elif('Yes. Congratulations, you found the exit door' in data):
            return self.foundExit()
        
        elif(not self.manual):
            print('PANIC! Manual Mode')
            self.manual = True
        
        return self.manualInput()
    
    def manualInput(self):
        msg = sys.stdin.readline()
        if (msg == (self.REANUDE_COMMAND + '\n')):
            self.manual = False
            return self.decideNextMove()
        
        if (msg.replace('\n', '') in directions):
            return self.goTo(msg.replace('\n', ''))
        
        return msg
    
    def blockedInput(self):
        self.map.setPos(self.attemptedPosition, self.map.TAKEN)
        self.plan = None
        return self.decideNextMove()
    
    def correctInput(self):
        self.map.moveTo(self.attemptedPosition)
        if (self.map.getPos(self.map.getCurrentPosition()) != self.map.FREE):
            self.map.setPos(self.attemptedPosition, self.map.DOUBT)
        return self.decideNextMove()
    
    def noExit(self):
        self.map.setPos(self.attemptedPosition, self.map.FREE)
        return self.decideNextMove()
    
    def foundExit(self):
        self.map.setPos(self.attemptedPosition, self.map.EXIT)
        return self.STOP_COMMAND + '\n'
    
    def decideNextMove(self):
        currentCell = self.map.getPos(self.map.getCurrentPosition())
        
        if (self.manual):
            return self.manualInput()
        
        if (currentCell == self.map.DOUBT):
            return self.IS_EXIT_COMMAND + '\n'
        
        if (self.plan == None):
            objectivePos = self.map.getExitPosition()
            if (objectivePos == None):
                objectivePos = (self.map._height - 1, self.map._width - 1)
            self.plan = self.map.MakePlanToReach(objectivePos)
        
        if (self.plan != None and len(self.plan)  > 0):
            nextpos = self.plan[0]
            self.plan.pop(0)
            direction = self.directionByMovement(nextpos[0] - self.map.x, nextpos[1] - self.map.y)
            
            return self.goTo(directions[direction])
        
        # return self.goTo(self.randomDirection())
        return self.manualInput()
    
    def goTo(self, directionString):
        self.lastMovement = directions.index(directionString)
        self.attemptedPosition = self.map.positionAfterMovement(self.lastMovement)
        return directionString + '\n'
    
    def randomDirection(self):
        randomInt = random.randint(0,len(directions)-1)
        return directions[randomInt]
    
    def directionByMovement(self, x, y):
        if x > 1:
            x = x - self.map._height
        elif x < -1:
            x = x + self.map._height

        if y > 1:
            y = y - self.map._width
        elif y < -1:
            y = y + self.map._width

        if (x == 0 and y == 1):
            return 0
        elif (x == 1 and y == 0):
            return 1
        elif (x == 0 and y == -1):
            return 2
        elif (x == -1 and y == 0):
            return 3
        else:
            return -1

class Movement:
    def __init__(self, nx, ny, dst, lastmove):
        self.x = nx
        self.y = ny
        self.distance = dst
        self.path = []

        if (lastmove != None):
            for i in lastmove.path:
                self.path.append(i)

        self.path.append([self.x, self.y])

class Map:
    def __init__(self):
        self.filename = "map.txt"
        
        self.UNKOWN = '-'
        self.FREE = ' '
        self.TAKEN = 'X'
        self.DOUBT = '?'
        self.EXIT = 'E'
        
        self._height = 50
        self._width = 50

        self.x = int(0)
        self.y = int(0)
        
        self.resetMap()
        
    def resetMap(self):
        self.map = [[0 for x in range(self._height)] for y in range(self._width)]
        for i in range (self._height):
            for j in range(self._width):
                self.map[i][j] = self.UNKOWN
        self.map[self.x][self.y] = self.FREE
    
    def getPos(self, position):
        return self.map[position[0]][position[1]]
    
    def setPos(self, position, value):
        if (self.getPos(position) != value):
            self.map[position[0]][position[1]] = value
            self.writeMap()
    
    def moveTo(self, position):
        self.x = position[0]
        self.y = position[1]
    
    def getCurrentPosition(self):
        return (self.x, self.y)
    
    def positionAfterMovement(self, direction):
        if   (direction == 0):
            return (self.x, self.y + 1)
        elif (direction == 1):
            return (self.x + 1, self.y)
        elif (direction == 2):
            return (self.x, self.y - 1)
        elif (direction == 3):
            return (self.x - 1, self.y)
        
        raise ValueError(f'The provided direction is not allowed: {direction}')
        
    def getExitPosition(self):
        for i in range (self._height):
            for j in range(self._width):
                if (self.map[i][j] == self.EXIT):
                    return (i, j)
        return None
        
    def MakePlanToReach(self, objectivePosition):
        self.objective = objectivePosition
        
        self.visited = [[0 for x in range(self._height)] for y in range(self._width)]
        for i in range (self._height):
            for j in range(self._width):
                self.visited[i][j] = False

        self.plan = []
        self.plan.append(Movement(self.x, self.y, 0, None))

        selectplan = None
        while (len(self.plan) > 0 and selectplan == None):
            #print len(self.plan)
            nextmove = self.plan[0]
            self.plan.pop(0)

            if ((nextmove.x, nextmove.y) == self.objective):
                selectplan = nextmove.path
            else:
                self.ProccessMovement(nextmove)

        self.plan = selectplan
        if (self.plan != None):
            print ('A new plan has been calculated')
            print (selectplan)
            self.plan.pop(0)
        else:
            print('No possible plan was found')
        
        return self.plan
        
    def ProccessMovement(self, move):
        self.visited[move.x][move.y] = True

        px = [1, 0, -1, 0]
        py = [0, 1, 0, -1]

        #print "Processing node: " + str(move.x) + " " + str(move.y)

        for i in range(len(px)):
            x = (move.x + px[i]) % self._height
            y = (move.y + py[i]) % self._width
            if self.CellIsValid(x, y) and (self.visited[x][y] == False):
                self.visited[x][y] = True
                nextmove = Movement(x, y, self.DistanceToObjective(x, y), move)
                self.plan.append(nextmove)
                #print "accepted: " + str(x) + " " + str(y)
            #else:
                #print "not accepted: " + str(x) + " " + str(y)

        def OrderByDistance(m):
            return m.distance
        
        self.plan.sort(key=OrderByDistance)
    
    def CellIsValid(self, x, y):
        return x >= 0 and x < self._height and y >= 0 and y < self._width and self.map[x][y] != self.TAKEN
    
    def DistanceToObjective(self, x, y):
        dx = abs(x - self.objective[0])
        if (dx > self._height):
            dx = self._height - dx
        dy = abs(y - self.objective[1])
        if (dy > self._width):
            dy = self._width - dy
        return dx*dx + dy*dy
    
    def loadMap(self):
        self.resetMap()
        
        try:
            with open(self.filename, "r") as f:
                for i in range(self._height):
                    line = f.readline()
                    for j in range(self._width):
                        self.map[i][j] = line[j]
        except FileNotFoundError:
            print('Map file not found, creating one')
            self.writeMap()

    def writeMap(self):
        f = open(self.filename, "w")
        for i in range (self._height):
            for j in range(self._width):
                f.write(self.map[i][j])
            f.write('\n')
        f.close()

import socket, select, sys
class SSHConnecter:
    def __init__(self, host, port):
        self.stopCommand = 'STOP'
        self.host = host
        self.port = port
    
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
        
        # connect to remote host
        try :
          self.s.connect((self.host, self.port))
          print ('Connected to remote host ' + self.host + ' : ' + str(self.port))
          
        except :
          print ('Unable to connect')
          return False
      
        return True
        
    def manualControl(self):
        def getInput(data):
            return sys.stdin.readline()
        
        return self.automaticControl(getInput)
                    
    def automaticControl(self, sshFunction):
        while 1:
            socket_list = [self.s]
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
            
            data = self.s.recv(4096).decode('utf-8')
            if not data :
                print ('Connection closed')
                return False
            else :
                sys.stdout.write(data)
                
                msg = sshFunction(data)
                
                if (msg == (self.stopCommand + '\n')):
                    return True
                else:
                    sys.stdout.write(msg)
                    self.s.send(str.encode(msg))

def main():
    host = 'codechallenge-daemons.0x14.net'
    port = 4321
    
    outputfile = "output"
    
    dungeon = Dungeon()
    # dungeon.manual = True
    
    ssh = SSHConnecter(host, port)
    ssh.connect()
    ssh.automaticControl(dungeon.mainLoop)
    
    dungeon.map.x = 0
    dungeon.map.y = 0
    path = dungeon.map.MakePlanToReach(dungeon.map.getExitPosition())
    path.insert(0, (0, 0))
    
    print ('Path:')
    
    pathString = f'({path[0][0]}, {path[0][1]})'
    for position in path[1:]:
        pathString += f', ({position[0]}, {position[1]})'
        
    print (pathString)
    
    f = open(outputfile + '.txt', "w")
    f.write(pathString)
    f.close()
    
    print ('Exit')
    return
    

if __name__ == "__main__":
    main()
