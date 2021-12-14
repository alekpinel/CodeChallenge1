# coding=utf-8
'''
  13/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 3 - The night of the hunter
'''

def getValue(word, charValues):
    value = 0
    for char in word:
        value += charValues[char]
    return value

def processCase(case):
    # print (case)
    word1, word2 = case['Words']
    charValues = case['Values']

    value1 = getValue(word1, charValues)
    value2 = getValue(word2, charValues)

    if (value1 > value2):
        return word1
    elif (value2 > value1):
        return word2
    else:
        return '-'

def getFraction(input):
    if ('/' in input):
        integer1 = int (input.split('/')[0])
        integer2 = int (input.split('/')[1])
        return integer1 / integer2
    else:
        return int(input)

def decodifyCase1(input):
    dict = {}
    input = input.split('{')[1]
    input = input.split('}')[0]
    for value in input.split(','):
        char = value.split('\'')[1]
        decimal = getFraction(value.split(':')[1])
        dict[char] = decimal

    return dict

def decodifyCase2(input):
    dict = {}
    input = input.split('[')[1]
    input = input.split(']')[0]
    for value in input.split('(')[1:]:
        value = value.split(')')[0]
        char = value.split('\'')[1]
        decimal = getFraction(value.split(',')[1])
        dict[char] = decimal

    return dict

def decodifyCase3(input):
    dict = {}
    for value in input.split(','):
        char = value.split('=')[0]
        decimal = getFraction(value.split('=')[1])
        dict[char] = decimal

    return dict

def readCase(file):
    words, values = file.readline().split("|")
    words = words.split('-')

    if (values[0] == '{'):
        values = decodifyCase1(values)
    elif (values[0] == '['):
        values = decodifyCase2(values)
    else:
        values = decodifyCase3(values)

    case = {'Words':words, 'Values':values}
    return case

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "r")
    nlines = int(f.readline())
    lines = []
    for i in range(nlines):
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
