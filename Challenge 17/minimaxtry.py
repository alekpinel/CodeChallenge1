# coding=utf-8
'''
  19/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 17 - Super Digger Bros and the bulldozer of infinite buckets
'''

# This MINIMAX implementation is based in the code of:
# https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/

class Pile:
    def __init__(self, N):
        self.pile = N

class Game:
    def __init__(self, piles):
        self.players = ['Edu', 'Alberto']
        self.current_state = piles
        
        self.piles = []
        for i in piles:
            self.piles.append(Pile(i))
        
    def winnerAlgorithmic(self):
        (m, max_i, max_j) = self.max_alpha_beta(float('-inf'), float('inf'))
        
        if (m < 0):
            return self.players[1]
        else:
            return self.players[0]
        
        
    def possibleBuckets(self, pile):
        possibles = []
        bucket = 1
        while bucket <= self.current_state[pile]:
            possibles.append(bucket)
            bucket *= 2
        possibles.reverse()
        return possibles
    
    def onlyOnePile(self):
        pile = None
        for i in self.current_state:
            if (pile != None):
                return None
            pile = i
        return pile
    
    def isFinished(self):
        for i in self.current_state:
            if i > 0:
                return False
        return True
    
    def max_alpha_beta(self, alpha, beta):
        maxv = float('-inf')
        pile = None
        bucket = None
    
        if (self.isFinished()):
            return (-1, 0, 0)
        
        onlyPile = self.onlyOnePile()
        if (onlyPile != None):
            if (onlyPile % 3 == 0):
                return (-1, 0, 0)
            else:
                return (1, 0, 0)
    
        for i in range(0, len(self.current_state)):
            for j in self.possibleBuckets(i):
                self.current_state[i] -= j
                (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                
                if m > maxv:
                    maxv = m
                    pile = i
                    bucket = j
                self.current_state[i] += j
    
                if maxv >= beta:
                    return (maxv, pile, bucket)
    
                if maxv > alpha:
                    alpha = maxv
    
        return (maxv, pile, bucket)
    
    def min_alpha_beta(self, alpha, beta):
       minv = float('inf')
    
       pile = None
       bucket = None
    
       if (self.isFinished()):
           return (1, 0, 0)
    
       for i in range(0, len(self.current_state)):
           for j in self.possibleBuckets(i):
                self.current_state[i] -= j
                (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                if m < minv:
                    minv = m
                    pile = i
                    bucket = j
                    
                self.current_state[i] += j
                
                if minv <= alpha:
                    return (minv, pile, bucket)
                
                if minv < beta:
                    beta = minv
    
       return (minv, pile, bucket)
        
def processCase(case):
    game = Game(case)
    winner = game.winnerAlgorithmic()
    return winner


def readCase(file):
    nPiles = int(file.readline())
    listOfPiles = file.readline().replace('\n', '').split(' ')
    listOfPiles = [int(x) for x in listOfPiles]
    return listOfPiles

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "r", encoding="utf-8")
    nlines = int(f.readline())
    lines = []
    for i in range(nlines):
        lines.append(caseProcessor(f))
    f.close()
    return lines

#Write the output
class OutputWriter:
    def __init__(self, outputfile):
        self.outputfile = None if outputfile == None else open(outputfile + ".txt", "w", encoding="utf-8");
        self.i = 0
        
    def __del__(self):
        if (self.outputfile != None):
            self.outputfile.close()

    def __call__(self, output):
        string = "Case #" + str(self.i + 1) + ": " + str(output) + "\n"
        self.i = self.i + 1
        print(string.replace("\n", ""))
        if (self.outputfile != None):
            self.outputfile.write(string)

def main():
    testType = 'toy'
    writeFile = False

    inputfile = testType + "Input"
    outputfile = testType + "Output"

    if (not writeFile):
        outputfile = None

    inputs = readInput(inputfile, readCase)


    outputWriter = OutputWriter(outputfile)
    for input in inputs:
        output = processCase(input)
        outputWriter(output)

if __name__ == "__main__":
    main()
