# coding=utf-8
'''
  19/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 17 - Super Digger Bros and the bulldozer of infinite buckets
'''

# When there is only one pile is very easy to know the winner.


class Game:
    def __init__(self, piles):
        self.players = ['Edu', 'Alberto']
        self.piles = piles

    def winnerAnalitic(self):
        initial_result = 1
        can_change = 0
        
        for pile in self.piles:
            if (pile % 3 == 0):
                initial_result *= 1
            else:
                initial_result *= -1
                
            if (pile % 3 == 2):
                can_change += 1
        
        can_change = can_change % 2
        
        #Player 1 wins
        if (initial_result < 0):
            return self.players[0]
        else:
            #Player 1 can change the pile
            if (can_change):
                return self.players[0]
            #Player 2 wins
            else:
                return self.players[1]

def processCase(case):
    game = Game(case)
    winner = game.winnerAnalitic()
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
    testType = 'submit'
    writeFile = True

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
