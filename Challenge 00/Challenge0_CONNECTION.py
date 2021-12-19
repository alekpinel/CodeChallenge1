# coding=utf-8
'''
  15/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 8 - Awesome Sales Inc.!
'''

import socket, select, sys

class Connection:
    def __init__(self):
        self.REANUDE_COMMAND = 'REANUDE'
        self.manual = True
        self.output = ''
    
    def mainLoop(self, data):
        self.readInput(data)
        return self.decideNextMove()
    
    def readInput(self, data):
        pass
    
    def decideNextMove(self):
        if (self.manual):
            return self.manualInput()
        
        return 'No Input'
    
    def manualInput(self):
        msg = sys.stdin.readline()
        if (msg == (self.REANUDE_COMMAND + '\n')):
            self.manual = False
            return self.decideNextMove()
        return msg
    
    def getFinalOutput(self):
        return self.output


class SSHConnecter:
    def __init__(self, host, port):
        self.STOP_COMMAND = 'STOP'
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
                
                if (msg == (self.STOP_COMMAND + '\n')):
                    return True
                else:
                    sys.stdout.write(msg)
                    self.s.send(str.encode(msg))

def writeOutput(filename, output):
    f = open(filename + '.txt', "w")
    f.write(output)
    f.close()

def main():
    host = 'codechallenge-daemons.0x14.net'
    port = 7162
    
    outputfile = "Output"
    writeFile = True
    
    connection = Connection()
    
    ssh = SSHConnecter(host, port)
    ssh.connect()
    ssh.automaticControl(connection.mainLoop)
    
    if (writeFile):
        writeOutput(outputfile, connection.getFinalOutput())

if __name__ == "__main__":
    main()
