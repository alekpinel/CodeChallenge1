# coding=utf-8
'''
  13/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 5 - Invictus
'''

def processCase(case):
    print (case)
    
    return case


def readCase(file):
    case = []
    for i in range(24):
        case.append(file.readline())
    return case

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "r")
    nCases = 1
    lines = []
    for i in range(nCases):
        lines.append(caseProcessor(f))
    f.close()
    return lines

#Write the output
class OutputWriter:
    def __init__(self, outputfile):
        self.outputfile = None if outputfile == None else open(outputfile + ".txt", "w");
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
    main();
