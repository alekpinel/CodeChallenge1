# coding=utf-8
'''
  13/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 5 - Invictus
'''

def getDistance(numbers):
    distance = []
    for i in range(len(numbers) - 1):
        distance.append(numbers[i + 1] - numbers[i])
    return distance

def processCase(case):
    # print (case)
    bytes = [ord(i) for i in case]
    print(len(bytes))
    interestingNumbers = list(filter(lambda value: value >= 127, bytes))
    
    mandela = ["M", "A", "N", "D", "E", "L", "A"]
    mandelaBytes = [ord(i) for i in mandela]
    
    decodified = []
    for i in range(len(interestingNumbers) - 1):
        decodified.append(interestingNumbers[i + 1] - interestingNumbers[i])
        
    # print (getDistance(bytes))
    
    return None


def readCase(file):
    chars = []
    while 1:
      byte_s = file.read(1)
      if not byte_s:
         break
      chars.append(byte_s)
      
    return chars

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "rb")
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
    writeFile = True

    inputfile = "Invictus2"
    outputfile = "Output"

    if (not writeFile):
        outputfile = None

    inputs = readInput(inputfile, readCase)

    outputWriter = OutputWriter(outputfile)
    for input in inputs:
        output = processCase(input)
        outputWriter(output)

if __name__ == "__main__":
    main();
