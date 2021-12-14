# coding=utf-8
'''
  13/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 1 - Roll the dice!
'''

def processData(data):
    player1 = data[0] + data[1]
    player2 = player1 + 1
    if (player2 > 12):
        return '-'
    return player2

def readLine(line):
    results = line.split(":")
    return [int(i) for i in results]

#Get input
def readInput(inputfile, lineProcessor):
    f = open(inputfile + ".txt", "r")
    nlines = int(f.readline())
    lines = []
    for i in range(nlines):
        lines.append(lineProcessor(f.readline().replace("\n", "")))
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
    isSubmit = True
    writeFile = True

    if (isSubmit):
        inputfile = "submitInput"
        outputfile = "submitOutput"
    else:
        inputfile = "testInput"
        outputfile = "testOutput"

    if (not writeFile):
        outputfile = None

    inputs = readInput(inputfile, readLine)

    outputWriter = OutputWriter(outputfile)
    for input in inputs:
        output = processData(input)
        outputWriter(output)

if __name__ == "__main__":
    main()
