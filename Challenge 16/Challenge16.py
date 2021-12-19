# coding=utf-8
'''
  19/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 16 - Where are the primes at?
'''

import socket, select, sys

PRIMES_10 = [2, 3, 5, 7]
PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

class Index:
    def __init__(self, index):
        self.index = index
        self.divisors = []
        self.priority = 0
        self.checkedTo = []
        
    def selectNextCheck(self, others):
        for other in others:
            if other != self and other not in self.checkedTo:
                return other
        return None
    
    def addDivisor(self, divisor, other_index):
        if (divisor != 1 and divisor not in self.divisors):
            self.divisors.append(divisor)
            
        if (other_index != self and other_index not in self.checkedTo):
            self.checkedTo.append(other_index)
        
        if (len(self.divisors) > 1 or (len(self.divisors) == 1 and self.divisors[0] not in PRIMES_10)):
            self.priority += 1

class Connection:
    def __init__(self):
        self.REANUDE_COMMAND = 'REANUDE'
        self.manual = False
        self.output = ''
        
        self.N = self.Q = None
        self.lastAsked = [None, None]
        self.finnished = False
    
    def mainLoop(self, data):
        self.readInput(data)
        return self.decideNextMove()
    
    def readInput(self, data):
        if (self.N == None or self.Q == None):
            numbers = data.split(' ')
            self.initialize(int(numbers[0]), int(numbers[1]))
        elif ('Oh no! You missed!' in data):
            self.finnished = True
            print(data)
            self.postMorten(data)
        elif ('Congratulations' in data):
            self.finnished = True
            print(data)
            self.output = data.split(' ')[-1]
        else:
            divisor = int(data)
            index_1, index_2 = self.lastAsked
            index_1.addDivisor(divisor, index_2)
            index_2.addDivisor(divisor, index_1)
            self.interpreteResult(index_1)
            self.interpreteResult(index_2)
    
    def markAsNonPrime(self, index):
        self.nonprimes.append(index)
        if (index in self.unknown):
            self.unknown.remove(index)
        print(f'Index {index.index} is not a prime')
    
    def markAsPrime(self, index):
        self.primes.append(index)
        # self.unknown.remove(index)
        print(f'Index {index.index} is a prime!')
        print(f'Primes {self.primesArray()}')
    
    def canBeConsiderPrime(self, index):
        if (len(index.divisors) == 0):
            return True
        value = index.divisors[0]
        squares = []
        square = value * value
        while square <= self.N:
            squares.append(square)
            square = square * value
        
        for square in squares:
            found = False
            for nonprime in self.nonprimes:
                if (square in nonprime.divisors):
                    found = True
                    
            if (not found):
                return False
        
        return True
    
    def interpreteResult(self, index):
        if (len(index.divisors) > 1):
            self.markAsNonPrime(index)
        elif(len(index.divisors) == 1 and index.divisors[0] not in PRIMES_100):
            self.markAsNonPrime(index)
    
    def primesArray(self):
        primes = '['
        for i in self.primes:
            primes += f'{i.index}, '
            
        if (len(self.primes) > 0):
            primes = primes[:-2]
        return primes + ']'
    
    def decideNextMove(self):
        if (self.finnished):
            return 'END\n'
        
        if (self.manual):
            return self.manualInput()
        
        indices_to_search = None
        while indices_to_search == None:
            if (len(self.primes) == len(PRIMES_100) + 1):
                indices_string = self.givePrimeIndices()
                print(indices_string)
                return indices_string
            
            indices_to_search = self.searchForImportant()
        index_1, index_2 = indices_to_search
        self.lastAsked = [index_1, index_2]
        
        return f'? {index_1.index} {index_2.index}\n'
    
    def manualInput(self):
        msg = sys.stdin.readline()
        if (msg == (self.REANUDE_COMMAND + '\n')):
            self.manual = False
            return self.decideNextMove()
        return msg
    
    def getFinalOutput(self):
        return self.output
    
    def initialize(self, N, Q):
        self.N = N
        self.Q = Q
        
        self.indices = []
        self.primes = []
        self.nonprimes = []
        self.unknown = []
        for i in range(1, N + 1):
            index = Index(i)
            self.indices.append(index)
            self.unknown.append(index)
            
    def searchForImportant(self):
        self.unknown.sort(key=lambda x: x.priority)
        
        for i in self.unknown:
            index = i
            if (index not in self.primes):
                break
            
        other = index.selectNextCheck(self.unknown)
        
        if (other == None):
            if (self.canBeConsiderPrime(index)):
                self.markAsPrime(index)
                return None
            else:
                other = index.selectNextCheck(self.nonprimes)
        
        if (other == None):
            self.markAsPrime(index)
            return None
        
        return [index, other]

    def givePrimeIndices(self):
        msg = '! '
        self.primes.sort(key=lambda x: x.index)
        for i in self.primes:
            msg += f'{i.index} '
        return msg + '\n'
    
    def postMorten(self, data):
        original = data.split('[')[1].split(']')[0].split(', ')
        for prime_index in self.primes:
            i = prime_index.index
            print(f'{i}: {original[i-1]}')
            if (int(original[i-1]) != 1 and int(original[i-1]) not in PRIMES_100):
                print(f'ERROR IN {i}: {original[i-1]}')


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
                # sys.stdout.write(data)
                
                msg = sshFunction(data)
                
                if (msg == (self.STOP_COMMAND + '\n')):
                    return True
                else:
                    # sys.stdout.write(msg)
                    self.s.send(str.encode(msg))

def writeOutput(filename, output):
    f = open(filename + '.txt', "w")
    f.write(output)
    f.close()

def main():
    
    # indices = [6, 15, 28, 38, 52, 54, 57, 61, 62, 64, 73, 75, 82, 87, 94, 97, 99, 13, 32, 77, 34, 19, 84, 22, 9]
    # original = [45, 52, 80, 58, 60, 2, 78, 9, 47, 4, 62, 84, 37, 94, 67, 69, 85, 90, 43, 8, 55, 17, 22, 38, 34, 100, 33, 5, 35, 98, 44, 41, 87, 11, 72, 18, 6, 7, 95, 92, 91, 25, 48, 39, 88, 86, 31, 93, 65, 36, 32, 83, 50, 53, 46, 70, 73, 64, 82, 40, 3, 29, 57, 97, 77, 12, 21, 96, 63, 51, 74, 81, 79, 15, 89, 99, 19, 75, 10, 30, 16, 59, 27, 23, 42, 68, 71, 28, 49, 56, 66, 26, 54, 13, 14, 24, 61, 20, 1, 76]
    # for i in indices:
    #     print(f'{i}: {original[i-1]}')
    #     if (int(original[i-1]) != 1 and int(original[i-1]) not in PRIMES_100):
    #         print(f'ERROR IN {i}: {original[i-1]}')
    # return 
    
    host = 'codechallenge-daemons.0x14.net'
    port = 7162
    
    outputfile = "Output"
    writeFile = True
    
    output_result = ''
    
    # while output_result == '':
    connection = Connection()
    
    ssh = SSHConnecter(host, port)
    ssh.connect()
    ssh.automaticControl(connection.mainLoop)
    
    output_result = connection.getFinalOutput()
    
    if (writeFile):
        writeOutput(outputfile, output_result)

if __name__ == "__main__":
    main()
