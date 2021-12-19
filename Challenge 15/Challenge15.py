# coding=utf-8
'''
  19/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 15 - The revenge of the non-Tuentistic numbers
'''

LAST_VALUE = [1, 1]

def processCase(N):
    
    # print(N)
    
    M = 100000007
    
    if (N > M):
        return 0
    
    value = 1
    i  = 1
    
    if (LAST_VALUE[0] < N + 1):
        i = LAST_VALUE[0]
        value = LAST_VALUE[1]
    
    while (i < N+1):
        value = (value * i) % M
        i += 1
        
        if (i % 100000000 == 20000000):
            i += 10000000
        if (i % 100000 == 20000):
            i += 10000
        if (i % 100 == 20):
            i += 10
    
    LAST_VALUE[0] = i
    LAST_VALUE[1] = value
    
    return value


def readCase(file):
    N = int(file.readline())
    return N

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
    testType = 'test'
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
